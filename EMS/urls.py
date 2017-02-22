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

]
