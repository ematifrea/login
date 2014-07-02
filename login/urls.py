from django.conf.urls import patterns, url
from login import views

urlpatterns = patterns('',
    url(r'^$', views.login, name='login'),
    # url(r'^home/$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
)