from django.conf.urls import patterns, url
from login import views
from login.views import UserEmailResetPassword, UserResetPassword

urlpatterns = patterns('',
    url(r'^$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^activate/(?P<activation_key>.+)/$', views.activate, name = 'activate'),
    url(r'^reset-password/(?P<account_name>\w+)/$', UserEmailResetPassword.as_view(), name='email_for_reset'),
    url(r'^reset-password/(?P<uidb64>.+)/(?P<token>.+)/$', UserResetPassword.as_view(), name='reset_password'),

)