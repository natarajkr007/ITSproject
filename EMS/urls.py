from django.conf.urls import url

from . import views

app_name = 'EMS'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^profile/$', views.user_profile, name='profile'),
    url(r'^monitor/$', views.monitor,name='monitor'),
    url(r'^forum/$', views.forum,name='forum'),
    url(r'^insert/$', views.insert,name='insert'),
    url(r'^show/$', views.show,name='show'),
    url(r'^search/$', views.search,name='search'),
    url(r'^search_show/$', views.search_show,name='search_show'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^user_dashboard/$', views.user_dashboard, name='user_dashboard'),
    url(r'^official_dashboard/$', views.official_dashboard, name='official_dashboard'),
    url(r'^message/$', views.message,name='message'),
    url(r'^accounts/login/$', views.user_login, name='login')

]
