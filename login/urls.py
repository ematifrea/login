from django.conf.urls import patterns, url
from login import views
from login.views import ResetPassword

urlpatterns = patterns('',
    url(r'^$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    # url(r'^reset-password/(?P<account_name>\w+)/$', ResetPassword.as_view(), name='reset'),
    url(r'^activate/(?P<activation_key>\w+)/$', views.activate, name = 'activate')
)