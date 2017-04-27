from django.conf.urls import url
from django.contrib.auth.views import login,logout

from . import views

urlpatterns = [
    # Login / Logout
    url(r'^login/$', login, {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^logout/$', logout, name='logout'),
    # ユーザー情報
    url(r'^profile/$', views.profile, name='profile'),
    # ユーザー登録
    url(r'^regist/$', views.regist, name='regist'),
    url(r'^regist_save/$', views.regist_save, name='regist_save'),
]
