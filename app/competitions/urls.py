from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # Comp
    url(r'^comps/$', views.CompList.as_view(), name='comp_list'),
    # Event
    url(r'^events/$', views.EventList.as_view(), name='event_list'),
    # Event Status
    url(r'^status/update/single/(?P<event_status_id>\S+)/$', views.update_event_status_single, name='event_status_update_single'),
    url(r'^status/update/(?P<comp_code>\S+)/$', views.update_event_status, name='event_status_update'),
    url(r'^status/(?P<comp_code>\S+)/$', views.EventStatusList.as_view(), name='event_status_list'),

]
