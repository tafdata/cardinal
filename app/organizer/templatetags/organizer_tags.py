import mojimoji

from django import template
from django.template.defaultfilters import stringfilter
register = template.Library()
from django.db.models.aggregates import Count
from django.utils import timezone # datetimeのwrapper


from competitions.models import Event, EventStatus
from organizer.models import Entry
from organizer.forms import EntryForm, EntryStatusEditForm

"""
記録の表示形式の変換
"""
@register.simple_tag
def format_mark(value, event):
    out = ""
    #正しく6桁で入力されている場合
    if len(value) == 6:
        num1, num2, num3 = int(value[0:2]), int(value[2:4]), int(value[4:])
        if not num1 == 0:
            if event.separator_1: out+=str(num1)+event.separator_1
            else: out += str(num1)
        if event.separator_2:
            if not num1 == 0 and num2 < 10:
                out+="0"+str(num2)+event.separator_2
            else: out+=str(num2)+event.separator_2
        else: out += str(num2)
        if event.separator_3:
            if not num3 == 0:
                if num3 >= 10: out+=str(num3)+event.separator_3
                else: out+='0'+str(num3)+event.separator_3
            else: out+= "00"+event.separator_3
        else:
            if not num3 == 0:
                if num3 >= 10: out+=str(num3)
                else:
                    print(num3)
                    out+='0'+str(num3)
            else: out+= "00"
        return out
    # 6桁で入力されていない場合
    return value



"""
実施種目EventStatusの一覧表
"""
@register.inclusion_tag('organizer/components/table_event_status.html')
def table_event_status(comp, user):
    # Param
    # - comp: 競技会

    event_statuss = EventStatus.objects.filter(comp=comp).order_by('start_list_priority', 'event__sex', '-section')
    event_s_list= []
    for event_status in event_statuss:
        entries = Entry.objects.filter(event_status=event_status)
        count_total = len(entries)
        entries_DNS = entries.filter(entry_status='DNS')
        count_DNS = len(entries_DNS)
        groups = entries.filter(group__gt=0).values_list('group', flat=True).order_by('group').distinct()
        event_s_list.append({'event_status': event_status, 'count': (count_total-count_DNS), 'count_total': count_total, 'count_DNS': count_DNS, 'count_group': len(groups)})        
    return {'comp':comp, 'event_list': event_s_list, 'user':user}
    
    
"""
種目Event別 一覧表
"""
@register.inclusion_tag('organizer/components/table_event.html')
def table_event(comp):
    # 種目が指定されていない場合は実施種目一覧を表示
    event_statuss = EventStatus.objects.filter(comp=comp)
    event_ids = event_statuss.values_list('event', flat=True).order_by('event').distinct()
    events = Event.objects.filter(id__in=event_ids).order_by('name')
    # 種目別スタートリストを出力可能か判定
    event_list = []
    for event in events:
        event_statuss_2 = EventStatus.objects.filter(comp=comp, event=event)
        VS_1, VS_2 = False, False
        OP_1, OP_2 = False, False
        for event_status in event_statuss_2:
            if event_status.section == 'VS':
                VS_1 = event_status.start_list
                VS_2 = event_status.start_list_2
            if event_status.section == 'OP':
                OP_1 = event_status.start_list
                OP_2 = event_status.start_list_2
        event_list.append({
            'event': event,
            'VS_1': VS_1,  'VS_2': VS_2,
            'OP_1': OP_1,  'OP_2': OP_2,
        })

    return {'event_list': event_list}


"""
Entry 個別登録
"""
@register.inclusion_tag('organizer/components/entry_add_single.html')
def entry_add_single(event_status=None, entry=False, submit_url=None):
    if entry:
        event_status = entry.event_status
        form = EntryForm(instance=entry, event_status=event_status)
    elif event_status:
        form = EntryForm(event_status=event_status)
    else:
        event_status = None
        form = EntryForm()

    return {'form': form, 'event_status':event_status, 'entry': entry, 'submit_url': submit_url}


        
"""
SL web
"""
@register.inclusion_tag('organizer/components/SL_web.html')
def start_list_web(comp, event_status, user):
    # 組数を取得
    group_nos = Entry.objects.filter(event_status=event_status).values('group').annotate(cnt=Count("*"),).order_by('group')

    # 組の仕分け[番組編成済み, 補欠, 番組編成未処理]
    groups_done, groups_sub, groups_null = [], [], []

    for group in group_nos:
        group["entries"] = Entry.objects.filter(event_status=event_status, group=group["group"]).order_by('order_lane', 'personal_best')    
        # 仕分け
        if group["group"] == -123: # 補欠
            groups_sub.append(group)
        elif group["group"] < 0: # 番組編成　未処理
            groups_null.append(group)
        else: # 番組編成　済み
            groups_done.append(group)

    return {'comp': comp, 'event_status': event_status,'user': user,
            'groups_done':groups_done,'groups_sub':groups_sub, 'groups_null':groups_null}

