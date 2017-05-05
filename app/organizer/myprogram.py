import numpy as np
import openpyxl as px
import pandas as pd
from openpyxl.styles import Font
from openpyxl.styles.colors import Color
from openpyxl.styles import Alignment
from openpyxl.styles import Border, Side

# Models
from competitions.models import Comp, Event, EventStatus
from organizer.models import Entry


class ProgramMaker:
    """
    Init
    """
    def _init__(self, *args, **kwargs):
        # Color
        color_default = Color(theme=1, tint=0.0)
        # Font
        self.font_default = Font(name='ＭＳ ゴシック',charset=128,family=3.0,b=False,i=False,strike=None,outline=None,shadow=None,condense=None,color=color_default,size=9,)
        self.font_small = Font(name='ＭＳ ゴシック',charset=128,size=6,)
        # Alignment
        self.al_default = Alignment(shrinkToFit=None, textRotation=0, vertical='center', horizontal='center', indent=0.0, justifyLastLine=None, relativeIndent=0.0, wrapText=None, readingOrder=0.0)
        self.al_wrap = Alignment(vertical='center', horizontal='center', wrapText=True)
        self.al_left = Alignment(vertical='center', horizontal='left')
        self.al_bottom = Alignment(vertical='bottom', horizontal='center')
        # Border
        thin = Side(border_style="thin", color="000000")
        self.border_bottom = Border(top=None, left=None, right=None, bottom=thin)
        self.border_all = Border(top=thin, left=thin, right=thin, bottom=thin)

        
    """
    Utils
    """
    def cell_posi(self, row, col):
        return col+str(row)


    def write_cell(self, cell, value, font=self.font_default, al=self.al_default, border=self.border_default):
        cell.value = value
        cell.font = font
        cell.alignment = al
        cell.border = border


    """
    Write Title
    """
    def write_title_Track(self, ws, row, event, GR=None):
        # 種目名
        ws.merge_cells(start_row=row,start_column=1,end_row=row+2,end_column=3)
        self.write_cell(ws.cell(row=row, column=1), GR.event)
        ws.cell(row=row, column=1).font = Font(size=24)
        # 大会記録
        if GR:        
            self.write_cell(ws.cell(row=row+1, column=4), '大会記録')
            self.write_cell(ws.cell(row=row+1, column=5), GR.mark) #記録
            self.write_cell(ws.cell(row=row+1, column=6), GR.name) #氏名
            self.write_cell(ws.cell(row=row+1, column=7), GR.club)#所属
            self.write_cell(ws.cell(row=row+1, column=8), GR.year) #年
        return row+3
        
        
    def write_title_HJPV(self, ws, row, GR=None):
        # 種目名
        ws.merge_cells(start_row=row,start_column=1,end_row=row+2,end_column=3)
        self.write_cell(ws.cell(row=row, column=1), GR.event)
        ws.cell(row=row, column=1).font = Font(size=24)
        # 大会記録
        if GR:
            self.write_cell(ws.cell(row=row+1, column=4), '大会記録')
            self.write_cell(ws.cell(row=row+1, column=5), GR.mark) #記録
            ws.merge_cells(start_row=row+1,start_column=6,end_row=row+2,end_column=11)
            self.write_cell(ws.cell(row=row+1, column=6), GR.name) #氏名
            ws.merge_cells(start_row=row+1,start_column=12,end_row=row+2,end_column=16)
            self.write_cell(ws.cell(row=row+1, column=12), GR.club)#所属
            ws.merge_cells(start_row=row+1,start_column=17,end_row=row+2,end_column=19)
            self.write_cell(ws.cell(row=row+1, column=17), GR.year) #年            
        return row+3

    
    def write_title_LJTJThrow(self, ws, row, GR=None):
        # 種目名
        ws.merge_cells(start_row=row,start_column=1,end_row=row+2,end_column=3)
        self.write_cell(ws.cell(row=row, column=1), GR.event)
        ws.cell(row=row, column=1).font = Font(size=24)
        # 大会記録
        if GR:
            self.write_cell(ws.cell(row=row+1, column=4), '大会記録')
            self.write_cell(ws.cell(row=row+1, column=5), GR.mark) #記録
            ws.merge_cells(start_row=row+1,start_column=6,end_row=row+2,end_column=7)
            self.write_cell(ws.cell(row=row+1, column=6), GR.name) #氏名
            self.write_cell(ws.cell(row=row+1, column=8), GR.club)#所属
            self.write_cell(ws.cell(row=row+1, column=9), GR.year) #年                 
        return row+3


    def write_title(self, ws, row, event, GR=None):
        # 部門        
        # エントリーを書き出し
        if event.event_type == 'Track8' or event.event_type == 'TrackN':
            row = self.write_title_Track(ws, row, GR)
        elif event.event_type == 'HJPV':
            row = self.write_title_HJPV(ws, row, GR)
        elif event.event_type == 'LJTJT' or event.event_type == 'Throw':
            row = self.write_title_LJTJ(ws, row, GR)       
        return row
    
    
    """
    Write Head
    """
    def write_head_Track(self, ws, row, group=True, wind=True):
        # 1行目
        if group:
            self.write_cell(ws.cell(row=row, column=1), str(group)+u"組")
        if wind:
            ws.merge_cells(start_row=row,start_column=9,end_row=row,end_column=11)
            self.write_cell(ws.cell(row=row, column=9), u"(風速＋･－　　　m/sec)") # Merged
        if group or  wind: # どちらかを書き込む場合は
            row += 1
        
        # 2行目
        self.write_cell(ws.cell(row=row, column=1), u"ﾚｰﾝ")
        self.write_cell(ws.cell(row=row, column=2), u"No.")
        print(cell_posi(row+1, "C")+":"+cell_posi(row+1,"D"))
        ws.merge_cells(cell_posi(row, "C")+":"+cell_posi(row,"D"))
        self.write_cell(ws.cell(row=row, column=3), u"氏名") # Merged
        self.write_cell(ws.cell(row=row, column=5), u"学年")
        self.write_cell(ws.cell(row=row, column=6), u"所属")
        self.write_cell(ws.cell(row=row, column=7), u"陸協")
        self.write_cell(ws.cell(row=row, column=8), u"所属")
        self.write_cell(ws.cell(row=row, column=9), u"順位")
        ws.merge_cells(cell_posi(row, "J")+":"+cell_posi(row,"K"))
        self.write_cell(ws.cell(row=row, column=10), u"記録")
        # 次の空白行の行番号を返す
        return row+1


    def write_head_Field(self, ws, row):
        # 試技順
        ws.merge_cells(cell_posi(row, "A")+":"+cell_posi(row+1,"A"))
        self.write_cell(ws.cell(row=row, column=1), u"試順", al=self.al_wrap)
        # No, 学年
        self.write_cell(ws.cell(row=row, column=2), u"No.")
        self.write_cell(ws.cell(row=row+1, column=2), u"学年")
        # 氏名, フリガナ
        ws.merge_cells(cell_posi(row, "C")+":"+cell_posi(row+1,"C"))
        self.write_cell(ws.cell(row=row, column=3), u"氏名") # Merged
        # 所属, 陸協
        self.write_cell(ws.cell(row=row, column=4), u"所属")
        self.write_cell(ws.cell(row=row+1, column=4), u"陸協")
        # 参考記録
        ws.merge_cells(cell_posi(row, "E")+":"+cell_posi(row+1,"E"))
        self.write_cell(ws.cell(row=row, column=5), u"参考\n記録", al=self.al_wrap)
        return row
        
        
    def write_head_HJPV(self, ws, row):
        # Feild共通ヘッダー
        row = self.write_Field_head(ws,row)
        # 試技
        for i in np.arange(6,33, 3):
            print(i)
            ws.merge_cells(start_row=row,start_column=i,end_row=row+1,end_column=i+2)
            self.write_cell(ws.cell(row=row, column=i), "m")
        ws.cell(row=row, column=i).alignment =Alignment(vertical='bottom', horizontal='center')
        # 記録
        ws.merge_cells(cell_posi(row, "AG")+":"+cell_posi(row+1,"AG"))
        self.write_cell(ws.cell(row=row, column=33), u"記録")
        # 順位
        ws.merge_cells(cell_posi(row, "AH")+":"+cell_posi(row+1,"AH"))
        self.write_cell(ws.cell(row=row, column=34), u"順位", al=self.al_wrap)
    
        # Borderの設定
        for i in range(1,35):
            ws.cell(row=row, column=i).border = self.border_all
            ws.cell(row=row+1, column=i).border = self.border_all   
            
        return row+2

    
    def write_head_LJTJThrow(self, ws, row, trial=6):
        # Feild共通ヘッダー
        row = self.write_Field_head(ws,row)
        # 試技&記録
        if trial == 6:
            cells = ["1", "2", "3",  u"3回目\nベスト", "4","5", "6",  u"記録"]
        else:
            cells = ["1", "2", "3", u"記録"]
            for i in np.arange(6,6+len(cells),1):
                print(i)
        ws.merge_cells(selftart_row=row,start_column=i,end_row=row+1,end_column=i)
        self.write_cell(ws.cell(row=row, column=i), cells[i-6], al=self.al_wrap)
        # 順位
        if trial == 6:
            ws.merge_cells(cell_posi(row, "N")+":"+cell_posi(row+1,"N"))
            self.write_cell(ws.cell(row=row, column=14), u"順位", al=self.al_wrap)
        else:
            ws.merge_cells(cell_posi(row, "J")+":"+cell_posi(row+1,"J"))
            self.write_cell(ws.cell(row=row, column=10), u"順位", al=self.al_wrap)
        
        # Borderの設定
        if trial == 6: cell_end = 14
        else: cell_end = 10
        for i in range(1,cell_end+1):
            ws.cell(row=row, column=i).border = self.border_all
            ws.cell(row=row+1, column=i).border = self.border_all   
            
        return row+2

    
    """
    Write Row
    """
    def write_row_Track(self, ws, row, entry, lane):
        self.write_cell(ws.cell(row=row, column=1), lane)
        self.write_cell(ws.cell(row=row, column=2), entry["bib"])
        self.write_cell(ws.cell(row=row, column=3), entry["name"])
        self.write_cell(ws.cell(row=row, column=4), entry["kana"])
        self.write_cell(ws.cell(row=row, column=5), entry["grade"])
        self.write_cell(ws.cell(row=row, column=6), entry["club"])
        self.write_cell(ws.cell(row=row, column=7), entry["jaaf_branch"])
        self.write_cell(ws.cell(row=row, column=8), entry["PB"])
        # 記録欄
        self.write_cell(ws.cell(row=row, column=9), "(   )")
        ws.cell(row=row, column=9).border = self.border_bottom
        ws.cell(row=row, column=10).border = self.border_bottom
        ws.cell(row=row, column=11).border = self.border_bottom
        return row+1
        


    def write_row_Field(self, ws,row, entry, order):
        # 試技順
        ws.merge_cells(cell_posi(row, "A")+":"+cell_posi(row+1,"A"))
        self.write_cell(ws.cell(row=row, column=1), order)
        # No, 学年
        self.write_cell(ws.cell(row=row, column=2), entry["bib"])
        self.write_cell(ws.cell(row=row+1, column=2), entry["grade"])
        # 氏名
        self.write_cell(ws.cell(row=row, column=3), entry["name"])
        self.write_cell(ws.cell(row=row+1, column=3), entry["kana"])
        # 所属, 陸協
        self.write_cell(ws.cell(row=row, column=4), entry["club"])
        self.write_cell(ws.cell(row=row+1, column=4), entry["jaaf_branch"])
        # 参考記録
        ws.merge_cells(cell_posi(row, "E")+":"+cell_posi(row+1,"E"))
        self.write_cell(ws.cell(row=row, column=5), entry["PB"])
        return row

    
            
    def write_row_HJPV(self, ws, row, entry, order):
        # Field 共通ヘッダー
        row = self.write_Field_head(ws, entry, order)
        # 試技
        for i in np.arange(6,33, 1):
            ws.merge_cells(start_row=row,start_column=i,end_row=row+1,end_column=i)
        # 記録
        ws.merge_cells(cell_posi(row, "AG")+":"+cell_posi(row+1,"AG"))
        # 順位
        ws.merge_cells(cell_posi(row, "AH")+":"+cell_posi(row+1,"AH"))
        
        # Borderの設定
        for i in range(1,35):
            ws.cell(row=row, column=i).border = self.border_all
            ws.cell(row=row+1, column=i).border = self.border_all
        return row+2


    def write_row_LJTJ(self, ws, row, entry, order, trial=6):
        # Field 共通ヘッダー
        row = self.write_Field_head(ws, entry, order)
        # 試技&記録
        if trial == 6: cell_end = 14
        else: cell_end = 10
        for i in np.arange(6,cell_end, 1):
            self.write_cell(ws.cell(row=row, column=i), "m", font=self.font_small)
            self.write_cell(ws.cell(row=row+1, column=i), "＋･－", font=self.font_small, al=self.al_left)        
        # 順位
        if trial == 6: ws.merge_cells(cell_posi(row, "N")+":"+cell_posi(row+1,"N"))
        else: ws.merge_cells(cell_posi(row, "J")+":"+cell_posi(row+1,"J"))
        
        # Borderの設定
        for i in range(1,cell_end+1):
            ws.cell(row=row, column=i).border = self.border_all
            ws.cell(row=row+1, column=i).border = self.border_all   
        return row + 2

    
    def write_row_Throw(self, ws, row, entry, order, trial=6):
        # 試技&記録
        if trial == 6: cell_end = 14
        else: cell_end = 10
        for i in np.arange(6,cell_end, 1):
            ws.merge_cells(start_row=row,start_column=i,end_row=row+1,end_column=i)
            self.write_cell(ws.cell(row=row, column=i), "m", al=self.al_bottom)
        # 順位
        if trial == 6: ws.merge_cells(cell_posi(row, "N")+":"+cell_posi(row+1,"N"))
        else: ws.merge_cells(cell_posi(row, "J")+":"+cell_posi(row+1,"J"))
        
        # Borderの設定
        for i in range(1,cell_end+1):
            ws.cell(row=row, column=i).border = self.border_all
            ws.cell(row=row+1, column=i).border = self.border_all   
        return row + 2

    
    """
    Write Group
    """
    def write_group_lane8(self, ws, row,  df, group=False, wind=True):
        # Params
        # - ws: worksheet
        # - row: 書き込み開始行番号
        # - df: dataFrame

        # Header
        row = self.write_track_head(ws, row, group)
        # エントリーの書き込み
        c = 0
        for i in [0,1,2,3,4,5,6,7]:
            row = self.write_track_row(ws, row, df.ix[i,:].to_dict(), i+1)
            c += 1
        # Finish
        print("> Write_group_lane8: write ", str(c), " entries")
        return row            

            
    # 長距離&補欠用
    def write_group_laneN(self, ws, row,  df, group=False, wind=True):
        # Params
        # - ws: worksheet
        # - row: 書き込み開始行番号
        # - df: dataFrame
        
        # Header
        row = self.write_head_Track(ws, row, group=group, wind=wind)
        # エントリーの書き込み
        c = 0
        for i in np.arange(0, len(df), 1):
            row = self.write_row_track(ws, row+i, df.ix[i,:].to_dict(), i+1)
            c += 1
        # Finish
        print("> Write_group_laneN: write ", str(c), " entries")
        return row


    def write_group_HJPV(self, ws, row,  df):
        # Header
        row = self.write_HJPV_head(ws, row)
        # エントリーの書き込み
        c = 0
        for i in import numpy as np.arange(0, len(df), 1):
            row = self.write_HJPV_row(ws, row, df.ix[i,:].to_dict(), i+1)
            c += 1
        # Finish
        print("> Write_group_HJPV: write ", str(c), " entries")
        return row


    def write_group_LJTJ(self, ws, row,  df, trial=6):
        # Header
        row = self.write_LJTJ_head(ws, row, trial=trial)
        # エントリーの書き込み
        c = 0
        for i in np.arange(0, len(df), 1):
            row = self.write_LJTJ_row(ws, row, df.ix[i,:].to_dict(), i+1, trial=trial)
            c += 1
        # Finish
        print("> Write_group_LJTJ: write ", str(c), " entries")            
        return row

            
    def write_group_Throw(self, ws, row,  df, trial=6):
        # Header
        row = self.write_LJTJThrow_head(ws, row, trial=trial)
        # エントリーの書き込み
        c = 0
        for i in np.arange(0, len(df), 1):
            row = self.write_Throw_row(ws, row, df.ix[i,:].to_dict(), i+1, trial=trial)
            c += 1
        # Finish
        print("> Write_group_Throw: write ", str(c), " entries")               
        return row        

    
    def write_groups(self, ws, row, event, Entries):
        groups = Entries.values('group').annotate(cnt=Count("*"),)        
        for gorup in groups:
            entries_g = Entries.filter(group=group["group"]).order_by('order_lane')
            # エントリーを書き出し
            if event.event_type == 'Track8':
                row = self.write_group_lane8(ws, row, entries_g, group=group["group"], wind=event.wind)
            elif event.event_type == 'TrackN':
                row = self.write_group_laneN(ws, row, entries_g, group=group["group"], wind=event.wind)
            elif event.event_type == 'HJPV':
                row = self.write_group_laneN(ws, row, entries_g, group=group["group"], wind=event.wind)
            elif event.event_type == 'LJTJ':
                row = self.write_group_laneN(ws, row, entries_g, group=group["group"], wind=event.wind)
            elif event.event_type == 'Throw':
                row = self.write_group_laneN(ws, row, entries_g, group=group["group"], wind=event.wind)                        
        return row

    
    """
    Sheet Styling
    """
    # Track
    def style_track(self, ws, row):
        # Params
        # - ws: worksheet
        # - row: The last row number of the page you edit (type=int)
        # - col:  The last col number of the page you edit (type=int)
    
        #　行の高さの指定
        for  i in range(0,row):
            ws.row_dimensions[i].height = 13
        #  列の幅の指定
        col_width = [("A", 4.0), ("B", 7.0), ("C", 11.0), ("D", 13.0), ("E", 7.0),  ("F", 11.0),("G", 7.0), ("H", 8.0), ("I", 5.0), ("J", 9.0), ("K", 9.0)]
        for t in col_width:
            ws.column_dimensions[t[0]].width = t[1]
        return row

        
    def style_HJPV(self, ws, row):
        # Params
        # - ws: worksheet
        # - row: The last row number of the page you edit (type=int)
        # - col:  The last col number of the page you edit (type=int)
    
        #　行の高さの指定
        for  i in range(0,row):
            ws.row_dimensions[i].height = 13
        #  列の幅の指定
        # [E-AF] = 1pt
        col_width = [("A", 3.0), ("B", 6.0), ("C", 11.0), ("D", 11.0), ("E", 5.0),  ("AG", 4.0),("AH", 3.0)]
        col_width_2 = 1.7
        for t in col_width:
            ws.column_dimensions[t[0]].width = t[1]
        for t in [chr(i) for i in range(65+5,65+26)]: # F - Z
            ws.column_dimensions[t].width = col_width_2
        for t in ["A"+chr(i) for i in range(65,65+6)]: #  AA- AF
            ws.column_dimensions[t]self.width = col_width_2
        return row
    
            
    def style_LJTJThrow(self, ws, row):
        # Params
        # - ws: worksheet
        # - row: The last row number of the page you edit (type=int)
        # - col:  The last col number of the page you edit (type=int)
        
        #　行の高さの指定
        for  i in range(0,row):
            ws.row_dimensions[i].height = 13
        #  列の幅の指定
        # [E-AF] = 1pt
        col_width = [("A", 3.0), ("B", 6.0), ("C", 10.0), ("D", 10.5), ("E", 5.0),  ("N", 4.0)]
        col_width_2 = 6.5
        for t in col_width:
            ws.column_dimensions[t[0]].width = t[1]
        for t in [chr(i) for i in range(65+5,65+13)]: # F - M
            ws.column_dimensions[t].width = col_width_2
        return row


    def style_sheet(self, ws, row, event):
        # 種目ごとに分岐
        if event.program_type == 'Track8' or event.program_type == 'TrackN':
            return self.style_Track(ws, row)
        elif event.program_type == 'HJPV':
            return self.style_LJThrow(ws, row)
        elif event.program_type == 'LJTJ' or event.program_type == 'Throw':
            return self.style_LJThrow(ws, row)

        
    def check_page(self, row, entry_num, type, title=True, ):
        # Param
        # - row: 書き始めの行番号
        # - entry_num: 書き込みエントリー数
        # - type: [ track, field ]
        row_page_max = 56       # 高さ13では56行で1ページ
        # Return
        # - 次に書き込む番号
        
        # 書き込みの最後の行の見積もり
        if type == 'track':
            row_end = entry_num + 2
        else:
            row_end = entry_num*2 + 2

        # 書き込むページ範囲を見積もり
        page_current = int(row/row_page_max)
        page_end = int(row_end/row_page_max)
        if row%row_page_max == 0: page_current = page_current - 1
        if row_end%row_page_max == 0: page_end = page_end - 1
        
        # ページをまたぐか否かの判断
        if page_current == page_end: # 改ページの必要なし
            return row
        elif page_current < page_end:
            return page_end * row_page_max

        
    """
    Write Event
    """
    def write_class(self, ws, row, class_name):
        # 部門名を書き出し
        ws.merge_cells(start_row=row,start_column=1,end_row=row,end_column=1)
        self.self.write_cell(ws.cell(row=row, column=1), "< "+class_name+" >")
        self.ws.cell(row=row, column=1).alignment = self.al_left
        return row+1
        
    def write_event(self, ws, event,GR=None,VS=False,Sub=False,OP=False):
        # Params
        # - ws: Worksheet
        # - event: Eventオブジェクト
        # - GR: 大会記録オブジェクト
        # - VS,SUb, OP: Entryオブジェクト(対校, 補欠, OP)

        # Title
        row = self.write_title(ws, event, GR)

        # 部門&レコード書き出し
        ## 対校
        if VS:
            row = self.write_class(ws, row, "対校")
            row = self.write_groups(ws, row, event, VS)            
        ## 補欠
        if Sub:
            row = self.write_class(ws, row, "補欠")
            row = self.write_groups(ws, row, event, Sub)
        ## OP
        if OP:
            row = self.write_class(ws, row, "オープン")
            row = self.write_groups(ws, row, event, OP) 

        return row


    """
    Write Sheet through Django Cardinal System
    """
    def cardinal_write_by_event(self, ws, row, comp, event):
        # Params
        # - wb, row: Workbook, 書き始めの行番号
        # - comp: Comp Object
        # - event: Event Object

        # Entry
        ## 対校
        try:
            event_status = EventStatus.objects.filter(comp=comp, event=event, section='VS')
            VS = Entry.objects.filter(event_status=event_status).order_by('group', 'order_lane')
        except (EventStatus.DoesNotExist, Entry.DoesNotExist) as e:
            VS = None
            print(e, "@cardinal_write_sheet_by_name")
        ## 補欠
        try:
            event_status = EventStatus.objects.filter(comp=comp, event=event, section='Sub')
            Sub = Entry.objects.filter(event_status=event_status).order_by('group', 'order_lane')
        except (EventStatus.DoesNotExist, Entry.DoesNotExist) as e:
            Sub = None
            print(e, "@cardinal_write_sheet_by_name")
        ## OP
        try:
            event_status = EventStatus.objects.filter(comp=comp, event=event, section='OP')
            OP = Entry.objects.filter(event_status=event_status).order_by('group', 'order_lane')
        except (EventStatus.DoesNotExist, Entry.DoesNotExist) as e:            
            OP = None
            print(e, "@cardinal_write_sheet_by_name")

        # 書き出し
        row = self.write_event(ws, event, VS=VS, Sub=Sub, OP=OP)
        return row
        

    def cardinal_write_by_event_status(self, ws, row, event_status):
        # Params
        # - wb, row: Workbook, 書き始めの行番号
        # - comp: Comp Object
        # - event: Event Object

        # 種目
        event = event_status.event

        # Entry
        try:
            entries = Entry.objects.filter(event_status=event_status).order_by('group', 'order_lane')
        except Entry.DoesNotExist as e:
            entries = None
            print(e, "@cardinal_write_sheet_by_name")
        # 部門
        if event_status.section == 'VS': VS = entries
        else: VS = None
        if event_status.section == 'Sub': Sub = entries
        else: Sub = None
        if event_status.section == 'OP': OP = entries
        else: OP = None
        
        # 書き出し
        row = self.write_event(ws, event, VS=VS, Sub=Sub, OP=OP)
        return row


    def cardinal_create_sheet_by_event(self, wb, event, sheet_name=None):
        # Create Sheet
        ws = wb.create_sheet()
        row = 1
        if sheet_name: ws.title = sheet_name

        # 書き出し
        row = self.cardinal_write_by_event(ws, row, event) 
        # シートのスタイリング
        row = self.style_sheet(ws, row, event)

        # シートの書き出し完了
        print("Success: write Excel Sheet of ", str(event))
        return True


    def cardinal_create_sheet_by_event_status(self, wb, event_status, sheet_name=None):
        # Create Sheet
        ws = wb.create_sheet()
        row = 1
        if sheet_name: ws.title = sheet_name

        # 書き出し
        event = event_status.event
        row = self.cardinal_write_by_event_status(ws, row, event_status) 
        # シートのスタイリング
        row = self.style_sheet(ws, row, event)

        # シートの書き出し完了
        print("Success: write Excel Sheet of ", str(event))
        return True    

    def cardinal_create_workbook_by_event(self, event):
        # Create new Workbook
        wb = px.Workbook()
        ws = wb.active
        ws.title = 'None'

        #書き出し
        self.cardinal_create_sheet_by_event(wb, event, sheet_name=str(event))
        # 完了
        return wb
        
        
        
