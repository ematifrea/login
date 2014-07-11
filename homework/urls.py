from django.conf.urls import patterns, include, url
from django.contrib import admin
from login.views import Index, Logout
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    url(r'^$', Index.as_view(), name='index'),
    url(r'^login/', include('login.urls', namespace='login')),
    url(r'^logout/', Logout.as_view(), name='logout'),
    url(r'^admin/', include(admin.site.urls)),
)
