from django.conf.urls import patterns, url
from login.views import UserEmailResetPassword, UserResetPassword,\
    Login, Register, Activate, UserProfile, Index

urlpatterns = patterns('',
    url(r'^$', Login.as_view(), name='login'),
    # url(r'^login/$', Login.as_view(), name='login'),
    url(r'^register/$', Register.as_view(), name='register'),
    url(r'^activate/(?P<activation_key>.+)/$', Activate.as_view(), name = 'activate'),
    url(r'^reset-password/account_name=(?P<account_name>\w+)/$', UserEmailResetPassword.as_view(), name='email_for_reset'),
    url(r'^profile/(?P<account_name>\w+)/$', UserProfile.as_view(), name='user_profile'),
    url(r'^reset-password/(?P<uidb64>.+)/(?P<token>.+)/$', UserResetPassword.as_view(), name='reset_password'),
)