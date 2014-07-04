from django.conf.urls import patterns, url
from login import views

urlpatterns = patterns('',
    url(r'^$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^user/(\d+)/$', views.user_index, name='user_index'),
)