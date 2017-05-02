from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.OrganizerIndex.as_view(), name='index'),
    url(r'^select/(?P<comp_code>\S+)/$', views.select_comp, name='select_comp'),
    # Entry
    url(r'^entry/$', views.EntryList.as_view(), name='entry_list'),
    url(r'^entry/add/$', views.entry_add, name='entry_add'),
]
