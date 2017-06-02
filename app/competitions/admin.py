from django.contrib import admin
from competitions.models import Comp, Event, EventStatus, GR, Result


# Register your models here.
"""
Comp
"""
class CompAdmin(admin.ModelAdmin):
    # 一覧に出したい項目
    list_display = ('code', 'name', 'place', 'date', 'status', 'created', 'modified',) 
    # 修正リンクでクリックできる項目
    list_display_links = ('code','name',)
admin.site.register(Comp,CompAdmin)


"""
Event
"""
class EventAdmin(admin.ModelAdmin):
    list_display = ('start_list_priority', 'name', 'sex', 'order', 'short', '_separator', 'created', 'modified',)
    list_display_links = ('name',)

    def _separator(self, row):
        record = ""
        if row.separator_1:
            record += "12"+row.separator_1
        if row.separator_2:
            record += "34"+row.separator_2
        if row.separator_3:
            record += "56"+row.separator_3
        else:
            record += "56"
        return record
admin.site.register(Event, EventAdmin)


"""
EventStatus
"""
class EventStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'comp', 'event', 'status',  'section', 'created', 'modified')
    list_display_links = ('comp', 'event',)
admin.site.register(EventStatus, EventStatusAdmin)


"""
GR
"""
class GRAdmin(admin.ModelAdmin):
    list_display = ('id', 'comp', 'event', 'mark',  'name_family', 'name_first', 'club', 'year', 'modified')
    list_display_links = ('id', 'comp', 'event',)
admin.site.register(GR, GRAdmin)


"""
Result
"""
class ResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'comp', 'event', 'sex', 'game_class', 'game_round', 'group', 'position', 'bib', 'name', 'club', 'mark', 'entry')
    list_display_links = ('game_class', 'game_round', 'group', 'position', 'name', 'club', 'mark')
admin.site.register(Result, ResultAdmin)
