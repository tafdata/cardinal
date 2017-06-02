import numpy as np
import pandas as pd
import mojimoji
import re
#import chardet                  # 文字コード判定


from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from competitions.models import Comp, Event, EventStatus, Result
from competitions.models import SECTION_CHOICES, SEX_CHOICES, ROUND_CHOICES
from organizer.models import Entry


"""
Base Class
"""
class UploadHandler(object):    
    def __init__(self, comp):
        self.comp = comp
        self.regex_mark()         # PBの正規表現パターンを保存
        self.errors = []
        self.errors_DB = []
        self.success_num = 0


    def regex_mark(self):
        # PBの正規表現パターンをコンパイル
        # 6-num: 数字６桁
        self.reg1 = re.compile(r"[0-9]{6}")
        # Readable Format
        self.reg2 = re.compile(r"[0-9]{1,2}('|\")[0-9]{2}\"[0-9]{2}") # 分+秒+1/100秒
        self.reg3 = re.compile(r"[0-9]{1,2}('|\")[0-9]{2}") # 秒+1/100秒
        self.reg4 = re.compile(r"[0-9]{1,2}m[0-9]{2}") # 距離        

        self.reg5 = re.compile(r"[0-9]{1,2}分[0-9]{2}秒[0-9]{2}") # 分+秒+1/100秒
        self.reg6 = re.compile(r"[0-9]{1,2}秒[0-9]{2}") # 分+秒+1/100秒
        

    #
    # Cleaning
    #
    def clean_sex(self, sex):
        # Param
        # - sex: ['男', '女']
        for t in SEX_CHOICES:
            if t[1] == sex: return t[0]
        # 不正入力
        raise ValueError("Invald 'sex' input.["+sex+"]")
        
        
    def clean_section(self, section):
        # Param
        # - section: ['VS', 'OP', 'TT', 'XX']
        # 部門の入力チェック
        for t in SECTION_CHOICES:
            if t[0] == section: return section
        # 不正入力
        raise ValueError("Invald 'section' input.["+section+"]")


    def clean_round(self, match_round):
        # Param
        # - section: ['Heats', 'Qualification', 'Semifinal', 'Final']
        # 部門の入力チェック
        for t in ROUND_CHOICES:
            if t[0] == match_round: return match_round
        # 不正入力
        raise ValueError("Invald 'round' input.["+match_round+"]")
        

    #
    # Object Selection
    #
    def select_event(self, event_name, sex):
        #  Eventを取得
        event = Event.objects.filter(name=event_name, sex=sex)
        if len(event) == 1: return event[0]    
        elif len(event) == 0: raise ValueError("No Event object. ["+event_name+","+sex+"]")
        else: raise ValueError("Too many Event objects. ["+event_name+","+sex+","+str(len(event))+"]")


    def select_event_status(self, comp, event, section, match_round):
        #  EventStatusを取得
        event_status = EventStatus.objects.filter(
            comp=comp,
            event=event,
            section=section,
            match_round=match_round,
        )
        if len(event_status) == 1: return event_status[0]
        elif len(event_status) == 0: raise ValueError("No EventStatus object. ["+str(comp)+","+str(event)+","+section+","+match_round+"]")
        else: raise ValueError("Too many EventStatus objects. ["+str(comp)+","+str(event)+","+section+","+match_round+","+str(len(event_status))+"]")
        


    #
    # Convert Error to CSV
    #
    def get_error_df(self):
        df_error = pd.DataFrame()
        df_error_DB = pd.DataFrame()

        # 通常エラー
        for error in self.errors:
            df_error = df_error.append(error["df"],ignore_index=True)
        if len(df_error) > 0:
            df_error = df_error[self.columns]
        # print(df_error)

        # DBエラー
        for error in self.errors_DB:
            df_error_DB = df_error_DB.append(error["df"],ignore_index=True)
        if len(df_error_DB) > 0:
            df_error_DB = df_error_DB[self.columns]
        # print(df_error_DB)
        
        return df_error, df_error_DB

        
"""
Cardinal形式エントリー CSVの処理
"""
class EntryHandler(UploadHandler):
    columns = ['secton', 'sex', 'event', 'round', 'group', 'order_lane', 'bib', 'name', 'kana', 'grade', 'club', 'jaaf_branch', 'PB']

    
    def __init__(self, comp, entry_status):        
        self.comp = comp
        self.entry_status = entry_status
        self.regex_pb()         # PBの正規表現パターンを保存
        self.errors = []
        self.success_num = 0
        
    def handle_csv(self, f):
        print("handle_csv called")
        df = pd.read_csv(f, dtype="object")
        df = df.fillna(False)
        self.check_csv_format(df)
        for i in range(len(df)):
            if self.regist_entry(df.ix[i,:].to_dict()):
                self.success_num += 1

        return self.errors        
    
    def check_csv_format(self, df):
        # カラム
        if not len(df.columns) == len(self.columns):        
            raise ValueError("Invalid CSV format, Column Num=("+str(len(df.columns))+","+str(len(self.columns))+")")
        

    #
    # Entry を一行ごと処理する
    #
    def regist_entry(self, df):
        # Param
        # -  df: len(df) must be 1        
        try:
            entry = Entry()

            # Eventの選択
            sex = self.clean_sex(df["sex"])
            event = self.select_event(df["event"], sex)
            #print(event)
            
            # EventStatusの選択
            section = self.clean_section(df["section"])
            match_round = self.clean_round(df["round"])
            #print("section, match_round:", section, match_round)
            event_status = self.select_event_status(self.comp, event, section, match_round)
        
            # Entry用Pramの準備
            name_family, name_first = self.clean_name(df["name"])
            kana_family, kana_first = self.clean_kana(df["kana"])        
            #print(name_family, name_first, kana_family, kana_first)
            pb = self.clean_PB(df["PB"])
            #print("PB: ", pb)
            #print("entry_status:", self.entry_status)
            group = df["group"]            
            if not group: group = -1
            order_lane = df["order_lane"]
            if not order_lane: order_lane = -1
            #print("group, order_lane: ", group, order_lane, type(group))
            #  Entry Object の作成
            if self.entry_status == 'Entry_2':
                check = True
            else:
                check = False
            entry = Entry.objects.create(
                event_status=event_status,
                bib=df["bib"],
                name_family=name_family,
                name_first=name_first,
                kana_family=kana_family,
                kana_first=kana_first,
                sex=sex,
                grade=df["grade"],
                club=df["club"],
                jaaf_branch=df["jaaf_branch"],
                personal_best=pb,
                group=group,
                order_lane=order_lane,
                entry_status=self.entry_status,
                check=check,
            )
            return True
        except ValueError as e:
            error = {'type': "ValueError", 'msg': str(e), 'df': df}
            #print(error["type"], ": ", error["msg"])
            self.errors.append(error)
        except KeyError as e:
            error = {'type': "KeyError", 'msg': str(e), 'df': df}
            #print(error["type"], ": ", error["msg"])
            self.errors.append(error)
        except IntegrityError as e:
            error = {'type': "IntegrityError[DB]", 'msg': str(e), 'df': df}
            #print(error["type"], ": ", error["msg"])
            self.errors.append(error)

        return False
        
    #
    # Cleaning
    # 
    def clean_name(self, name):
        if not name:
            raise ValueError("name == None")
        name = name.split(u"　")
        if len(name) == 2:
            name_family, name_first = name[0], name[1]
        else:
            name_family = name[0]
            name_first = ""
            for n in name[1:]:
                name_first += n+" "

        return name_family, name_first


    def clean_kana(self, kana):
        if not kana:
            raise ValueError("kana == None.")
        # 半角==>全角へ変換
        kana = mojimoji.han_to_zen(kana, digit=False, ascii=False)
        kana = kana.split()
        if len(kana) == 2: kana_family, kana_first = kana[0], kana[1]
        elif len(kana) == 1: kana_family, kana_first = kana[0], ''
        else:
            kana_family = kana[0]
            kana_first = ""
            for k in kana:
                kana_first += k+" "
        return kana_family, kana_first


    def clean_PB(self, PB):
        if not PB:
            raise ValueError("PB == None.")
        # 半角英数字に変換(全角が混ざった時用)
        PB = mojimoji.zen_to_han(PB)
        
        # reg1: 6-num
        m = self.reg1.fullmatch(PB)
        if m and m.span() == (0,6): return PB
        
        # reg2: Readable 12'34"56
        m = self.reg2.fullmatch(PB)
        if m:
            if m.span() == (0,8): return PB[0:2]+PB[3:5]+PB[6:]
            elif m.span() == (0,7): return "0"+PB[0]+PB[2:4]+PB[5:]
        
        # reg3: Readable 12"34
        m = self.reg3.fullmatch(PB)
        if m:
            if m.span() == (0,5): return "00"+PB[0:2]+PB[3:]
            elif m.span() == (0,4): return "000"+PB[0:1]+PB[2:]

        # reg4: Readable 12m34
        m = self.reg4.fullmatch(PB)
        if m:
            if m.span() == (0,5): return "00"+PB[0:2]+PB[3:]
            elif m.span() == (0,4): return "000"+PB[0:1]+PB[2:]

        raise ValueError("Invalid PB format. ["+PB+"]")
            
    def regex_pb(self):
        # PBの正規表現パターンをコンパイル
        # 6-num: 数字６桁
        self.reg1 = re.compile(r"[0-9]{6}")
        # Readable Format
        self.reg2 = re.compile(r"[0-9]{1,2}'[0-9]{2}\"[0-9]{2}") # 分+秒+1/100秒
        self.reg3 = re.compile(r"[0-9]{1,2}\"[0-9]{2}") # 秒+1/100秒
        self.reg4 = re.compile(r"[0-9]{1,2}m[0-9]{2}") # 距離

    
        
        




class ResultHandler(UploadHandler):
    columns = [
        'class', 'event', 'round',
        'group', 'position', 'order_lane', 'bib', 'name', 'kana', 'grade', 'club', 'space1', 'jaaf_branch', 'mark', 'wind',
        'space2', 'space3', 'space4',
    ]


    def handle_csv(self, f):
        print("handle_csv called")
        df = pd.read_csv(f, dtype="object",header=-1)
        df.columns = self.columns
        df = df.fillna(False)
        # print(df.head())
        # print(df.shape)
        for i in range(len(df)):
            if self.regist_result(df.ix[i,:].to_dict()):
                self.success_num += 1

        error_list = self.errors + self.errors_DB
        return error_list                
    

    
    def regist_result(self, df):
        # Param
        # - df: len(df) must be 1
        try:
            # 名前
            if df["name"] == False or len(df["name"]) == 0:
                return False
            # Classの記述形式
            if not df["class"] or not len(str(df["class"])) == 3:                
                raise ValueError("This expression type is not supported. (df['class']="+str(df['class'])+")")
            # 性別            
            sex = None
            if not df["class"].find(u'男') == -1:
                sex = 'M'
            elif not df["class"].find(u'女') == -1:
                sex = 'W'
            #print(sex)
            # Eventの選択
            event = self.select_event(df["event"], sex)
            #print(event)
            # 部門
            if not df["class"].find(u'対校') == -1: game_class = "VS"
            elif not df["class"].find(u'OP') == -1: game_class = "OP"
            #print(game_class)
            # ラウンド
            if df["round"] == u"決勝":   game_round = "Final"
            elif df["round"] == '予選':  game_round = "Heats"
            elif df["round"] == '準決勝': game_round = "Semifinal"
            # print(game_round)
            # 組
            group = int(df["group"])
            # 記録
            mark = self.clean_mark(str(df["mark"]).replace(" ", ""))
            #print(df["mark"], mark)
            # 風
            if df["wind"]:
                wind = str(df["wind"]).replace("m","")
            else:
                wind = False
            # print(wind)
            
            result =  Result.objects.create(
                comp=self.comp,
                event=event,
                sex=sex,
                game_class=game_class,
                game_round=game_round,
                group=group,
                position=df["position"],
                order_lane=df["order_lane"],
                bib=df["bib"],
                name=str(df["name"]),
                kana=mojimoji.han_to_zen(str(df["kana"]), digit=False, ascii=False),
                grade=df["grade"],
                club=df["club"],
                jaaf_branch=df["jaaf_branch"],
                mark=mark,
                wind=wind,                              
            )
            result.save()
        
        except ValueError as e:
            error = {'type': "ValueError", 'msg': str(e), 'df': df}
            #print(error["type"], ": ", error["msg"])
            self.errors.append(error)
            return False
        except KeyError as e:
            error = {'type': "KeyError", 'msg': str(e), 'df': df}
            #print(error["type"], ": ", error["msg"])
            self.errors.append(error)
            return False
        except IntegrityError as e:
            error = {'type': "IntegrityError[DB]", 'msg': str(e), 'df': df}
            #print(error["type"], ": ", error["msg"])
            self.errors_DB.append(error)
            return False

        # Entryがあればそれも登録
        try:
            if self.comp.cardinal_organizer == False:
                # Organizerを使用していない大会には, EntryObjectは存在しない
                return True

            name = str(result.name).split()
            entry = Entry.objects.filter(
                event_status__comp=self.comp,
                event_status__event=event,
                event_status__section=game_class,
                event_status__match_round=game_round,
                name_family=name[0],
                name_first=name[1],
                club=result.club,
            )
            if len(entry) == 1:
                entry = entry[0]
                result.entry = entry
                result.save()
                 # print(result.mark, entry.entry_status)
                if result.mark == 'DNS':
                    entry.entry_status = 'DNS'
                    # print(">> DNS:",entry, entry.entry_status)
                else:
                    entry.entry_status = 'Result'
                    # print(">> Result:", entry, entry.entry_status)
                entry.save()
                # print(entry, entry.entry_status)
            elif len(entry) == 0:
                # print(name)
                # 当日エントリーのEntry Objectを新規作成
                event_status = EventStatus.objects.filter(
                    comp=self.comp,
                    event=event,
                    section=game_class,
                    match_round=game_round,                    
                )
                if not len(event_status) == 1:
                    raise KeyError("EventStatus for Entry_2 does not exist or exist many.")

                kana = result.kana.split()
                if len(kana) < 2:
                    kana = ["",""]
                entry = Entry.objects.create(
                    event_status=event_status[0],
                    bib=df["bib"],
                    name_family=name[0],
                    name_first=name[1],
                    kana_family=kana[0],
                    kana_first=kana[1],
                    sex=result.sex,
                    grade=result.grade,
                    club=result.club,
                    jaaf_branch=result.jaaf_branch,
                    group=result.group,
                    order_lane=result.order_lane,
                    entry_status="Result",
                    check=True,
                    personal_best="000000"
                )
                result.entry = entry
                result.save()
            else:
                raise KeyError("ObjectDoesNotExist: Too many EventStatus for Entry_2.")           
        except KeyError as e:
            error = {'type': "KeyError", 'msg': str(e), 'df': df}
            #print(error["type"], ": ", error["msg"])
            self.errors.append(error)
        except IntegrityError as e:
            error = {'type': "IntegrityError[DB]", 'msg': str(e), 'df': df}
            #print(error["type"], ": ", error["msg"])
            self.errors_DB.append(error)          
        return True
            

    #
    # Cleaning
    #
    def clean_mark(self, mark):
        if not mark or mark == "False":
            return 'DNS'
        
        # reg6: Readable 12秒34
        m = self.reg6.fullmatch(mark)
        if m:
            if m.span() == (0,5): return "00"+mark[0:2]+mark[3:]
            elif m.span() == (0,4): return "000"+mark[0:1]+mark[2:]
                
        # reg5: Readable 12分34秒56
        m = self.reg5.fullmatch(mark)
        if m:
            if m.span() == (0,8): return mark[0:2]+mark[3:5]+mark[6:]
            elif m.span() == (0,7): return "0"+mark[0]+mark[2:4]+mark[5:]
            
        # reg4: Readable 12m34
        m = self.reg4.fullmatch(mark)
        if m:
            if m.span() == (0,5): return "00"+mark[0:2]+mark[3:]
            elif m.span() == (0,4): return "000"+mark[0:1]+mark[2:]

        print(mark, type(mark))
        raise ValueError("Invalid mark format. ["+mark+"]")            
        
            
