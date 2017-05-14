import numpy as np
import pandas as pd
import mojimoji
import re
#import chardet                  # 文字コード判定


from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.db import IntegrityError

from competitions.models import Comp, Event, EventStatus
from competitions.models import SECTION_CHOICES, SEX_CHOICES, ROUND_CHOICES
from organizer.models import Entry

class EntryHandler:
    def __init__(self, comp, entry_status):        
        self.columns = ['secton', 'sex', 'event', 'round', 'group', 'order_lane', 'bib', 'name', 'kana', 'grade', 'club', 'jaaf_branch', 'PB']
        self.comp = comp
        self.entry_status = entry_status
        self.regex_pb()         # PBの正規表現パターンを保存
        self.errors = []
        self.success_num = 0
        
    def handle_csv(self, f):
        print("handle_csv called")
        df = pd.read_csv(f)
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
        
        
