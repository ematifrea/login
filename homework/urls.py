from django.conf.urls import patterns, include, url
from django.contrib import admin
from login import views
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.login),
    url(r'^logout/$', views.logout),
    # url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^register/$', views.register),
    # url(r'^home/$', views.home),
    url(r'^admin/', include(admin.site.urls)),
)
