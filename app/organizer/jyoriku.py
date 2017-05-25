import numpy as np
import mojimoji
import pandas as pd

from django.db.models.aggregates import Count
from django.db.models import Max
from django.core.exceptions import ObjectDoesNotExist

# Models
from competitions.models import Comp, Event, EventStatus, GR as GRecord
from organizer.models import Entry
from organizer.templatetags.organizer_tags import format_mark
from organizer.templatetags.organizer_filters import zen_to_han, sex_to_ja, race_section_to_ja


"""
上陸連携　ツール
"""    
class JyorikuTool:
    def __init__(self, comp):
        self.comp = comp        # Comp オブジェクト
        
    
    """
    Cardinal System: BackUp用CSV
    """
    def start_list_cardinal(self):
        self.columns = ['section', 'sex', 'round', 'group', 'order_lane', 'event', 'bib', 'name', 'kana', 'grade', 'club', 'jaaf_branch', 'PB', 'entry_status']
        df = pd.DataFrame(columns=self.columns)

        # Entry オブジェクトの取得
        entries = Entry.objects.filter(event_status__comp=self.comp).order_by('event_status__event__name', '-event_status__section', 'event_status__event__sex', 'group', 'order_lane')
        for entry in entries:
            # print(entry)
            # 性別
            if entry.sex == 'M': sex = "男"
            elif entry.sex == 'W': sex = "女"
            else: sex = ""
            # 学年
            if entry.grade:grade = entry.grade
            else: grade = ""
            # 所属チーム
            if entry.club: club = entry.club
            else: club = ""
            # PB
            if entry.personal_best: pb = entry.personal_best
            else: pb = ""
            # Pandas Seriesを作成
            series = pd.Series([
                entry.event_status.section,
                sex,
                entry.event_status.match_round,
                entry.group,
                entry.order_lane,
                entry.event_status.event.name,
                entry.bib,
                entry.name_family+"\u3000"+entry.name_first,
                mojimoji.zen_to_han(entry.kana_family+"\u3000"+entry.kana_first),
                grade,
                club,
                entry.jaaf_branch,
                pb,
                entry.entry_status,
            ],index=self.columns)
            df = df.append(series, ignore_index = True)

        # d-type変換
        df[["group","order_lane"]]=df[["group","order_lane"]].astype(int)
        # print(df.head())
        # print(df.shape)

        return df

        



    """
    上陸用スタートリスト
    """
    def start_list_jyoriku(self):
        df = self.start_list_cardinal()
        # print(df[df['group'] < 0].index)
        df = df.drop(df[df['group'] < 0].index)
        print(df.head(20))

        # 上陸形式に変換
        ## 空白
        df["space1"] = ["" for i in range(len(df))]
        df["space2"] = ["" for i in range(len(df))]
        # print(df.columns)
        ## 部門
        for i in df[df["section"] == 'VS'].index:
            df.ix[i,"section"] = '対校'
        df["section"] = df["sex"] + df["section"]
        ## ゼッケン番号
        # print(df[df['bib'].str.find('-') >= 0])
        for i in df[df['bib'].str.find('-') >= 0].index:
            df.ix[i, 'bib'] = str(df.ix[i, 'bib']).replace('-', '')[:5]
        ## 所属カナ
        df["club_kana"] = ["" for i in range(len(df))]

        
        # 必要カラムの選択
        df = df.ix[:,['section', 'space1', 'event', 'group', 'order_lane', 'space2', 'bib', 'name', 'kana', 'grade', 'club', 'club_kana', 'jaaf_branch']]
        # print(df)
        
        return df
        
