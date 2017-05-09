from django.contrib import admin

from organizer.models import Entry


# Register your models here.
class EntryAdmin(admin.ModelAdmin):
    list_display = ['id', 'event_status', 'name_family', 'name_first', 'sex', 'club', 'personal_best', 'group', 'entry_status']
    list_display_link = ['id', 'event_status']
admin.site.register(Entry, EntryAdmin)
