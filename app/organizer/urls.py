from django.conf.urls import url

from . import views, viewsorganizer, viewsguest

urlpatterns = [
    url(r'^$', views.OrganizerIndex.as_view(), name='index'),
    url(r'^select/(?P<comp_code>\S+)/$', views.select_comp, name='select_comp'),
    # Entry
    # url(r'^entry/$', views.EntryList.as_view(), name='entry_list'),
    # url(r'^entry/add/$', views.entry_add, name='entry_add'),
    # url(r'^entry/add/file/$', views.entry_add_by_file, name='entry_add_by_file'),
    # Start List
    # url(r'^sl/$', views.sl_top, name='sl_top'),
    # url(r'^sl/(?P<event_status_id>\d+)/$', views.sl_top, name='sl_top'),
    # url(r'^sl/edit/(?P<event_status_id>\d+)/$', views.sl_edit, name='sl_edit'),
    # url(r'^sl/web/(?P<event_status_id>\d+)/$', views.sl_web, name='sl_web'),
    # url(r'^sl/excel/(?P<sl_type>\S+)/(?P<pk>\d+)/$', views.sl_excel, name='sl_excel'),

    # Organizer 運営者ページ
    url(r'^organizer/$', viewsorganizer.top, name='organizer_top'),
    url(r'^organizer/entry/single/(?P<entry_method>\S+)/(?P<id>\d+)/$', viewsorganizer.entry_add, name='organizer_entry_add'),
    url(r'^organizer/entry/single/(?P<entry_method>\S+)/$', viewsorganizer.entry_add, name='organizer_entry_add'),
    url(r'^organizer/entry/file/$', viewsorganizer.entry_add_by_file, name='organizer_entry_add_by_file'),    
    url(r'^organizer/sl/(?P<event_status_id>\d+)/$', viewsorganizer.SL_web, name='organizer_SL_web'),
    url(r'^organizer/sl/edit/(?P<event_status_id>\d+)/$', viewsorganizer.SL_edit, name='organizer_SL_edit'),
    url(r'^organizer/sl/update/(?P<event_status_id>\d+)/$', viewsorganizer.SL_update, name='organizer_SL_update'),
    url(r'^organizer/sl/excel/(?P<sl_type>\S+)/(?P<pk>\d+)/$', viewsorganizer.SL_excel, name='organizer_SL_excel'),
    url(r'^organizer/sl/excel/(?P<sl_type>\S+)/$', viewsorganizer.SL_excel, name='organizer_SL_excel'),
    url(r'^organizer/sl/jyoriku/$', viewsorganizer.SL_jyoriku, name='organizer_SL_jyoriku'),
    url(r'^organizer/sl/cardinal/$', viewsorganizer.SL_cardinal, name='organizer_SL_cardinal'),
    url(r'^organizer/result/import/$', viewsorganizer.result_import, name='organizer_result_import'),
    url(r'^organizer/result/excel/(?P<sl_type>\S+)/(?P<pk>\d+)/$', viewsorganizer.result_excel, name='organizer_result_excel'),
    url(r'^organizer/result/excel/(?P<sl_type>\S+)/$', viewsorganizer.result_excel, name='organizer_result_excel'),
    
    # Guestページ
    url(r'^guest/$', viewsguest.top, name='guest_top'),
    url(r'^guest/dns/(?P<entry_id>\d+)/$', viewsguest.DNS, name='guest_DNS'),
    url(r'^guest/sl/(?P<event_status_id>\d+)/$', viewsguest.SL_web, name='guest_SL_web'),
    url(r'^guest/entry/(?P<event_status_id>\d+)/$', viewsguest.entry_add, name='guest_entry_add'),

]
