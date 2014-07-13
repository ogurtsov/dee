from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'app.views.home', name='home'),
    url(r'^dashboard/$', 'app.views.dashboard', name='dashboard'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',{'next_page': '/'}, name="logout"),
    url(r'^admin/', include(admin.site.urls)),
)
