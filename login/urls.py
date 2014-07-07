from django.conf.urls import patterns, url
from login import views

urlpatterns = patterns('',
    url(r'^$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    # url(r'^confirm/$', views.confirm, name='confirm'),
    url(r'^activate/(?P<activation_key>\\w)/$', views.activate, name = 'activate')
)