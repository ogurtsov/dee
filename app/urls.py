from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
import views
import settings

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', 'app.views.home', name='home'),
    url(r'^dashboard/$', 'app.views.dashboard', name='dashboard'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',{'next_page': '/'}, name="logout"),
    url(r'^api/v1.0/directory/(?P<resource_id>\d+)[/]?$', login_required(views.Directories.as_view()), name='my_rest_view'),
    url(r'^api/v1.0/directory[/]?$', login_required(views.Directories.as_view()), name='my_rest_view'),
    url(r'^api/v1.0/file/(?P<resource_id>\d+)[/]?$', login_required(views.Files.as_view()), name='my_rest_view'),
    url(r'^api/v1.0/file[/]?$', login_required(views.Files.as_view()), name='my_rest_view'),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
