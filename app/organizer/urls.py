from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.OrganizerIndex.as_view(), name='index'),
    url(r'^select/(?P<comp_code>\S+)/$', views.select_comp, name='select_comp'),
    # Entry
    url(r'^entry/$', views.EntryList.as_view(), name='entry_list'),
    url(r'^entry/add/$', views.entry_add, name='entry_add'),
    url(r'^entry/add/file/$', views.entry_add_by_file, name='entry_add_by_file'),
    # Start List
    url(r'^sl/$', views.sl_top, name='sl_top'),
    url(r'^sl/(?P<event_status_id>\d+)/$', views.sl_top, name='sl_top'),
    url(r'^sl/edit/(?P<event_status_id>\d+)/$', views.sl_edit, name='sl_edit'),
    url(r'^sl/web/(?P<event_status_id>\d+)/$', views.sl_web, name='sl_web'),
    url(r'^sl/excel/(?P<sl_type>\S+)/(?P<pk>\d+)/$', views.sl_excel, name='sl_excel'),
]
