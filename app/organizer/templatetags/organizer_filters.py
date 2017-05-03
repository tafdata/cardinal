import mojimoji

from django import template
from django.template.defaultfilters import stringfilter
register = template.Library()

from competitions.models import Event


"""
レース区分の日本語置き換え Filer
"""

@register.filter(name='race_section_to_ja')
@stringfilter
def race_section_to_ja(value):
    if value == 'VS':
        return '対校'
    elif value == 'TT':
        return '記録会'
    elif value == 'XX':
        return 'その他'
    return value


"""
性別の日本語置き換え Filer
"""
@register.filter(name='sex_to_ja')
@stringfilter
def sex_to_ja(value):
    if value == 'M':
        return '男子'
    elif value == 'W':
        return '女子'
    elif value == 'F':
        return '家族'
    elif value == 'X':
        return 'その他'
    return value


"""
全角=>半角 変換
"""
@register.filter(name='zen_to_han')
@stringfilter
def zen_to_han(value):
    return mojimoji.zen_to_han(value)



"""
記録の表示形式の変換
"""
@register.filter(name='mark')
def mark(value, event):
    print(event)
    return str(value)+"["+event+"]"



