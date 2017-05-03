import mojimoji

from django import template
from django.template.defaultfilters import stringfilter
register = template.Library()

from competitions.models import Event



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
        if event.separator_2: out+=str(num2)+event.separator_2
        else: out += str(num2)
        if event.separator_3: out+=str(num3)+event.separator_3
        else: out += str(num3)
        return out
    # 6桁で入力されていない場合
    return value


