from django.conf.urls import patterns, include, url
from django.contrib import admin
from login import views
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.index, name='index'),
    url(r'^login/', include('login.urls', namespace='login')),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^admin/', include(admin.site.urls)),
)
