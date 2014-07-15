from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
import views
import settings

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', 'app.views.home', name='home'),
    url(r'^dashboard/$', 'app.views.dashboard', name='dashboard'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',{'next_page': '/'}, name="logout"),
    url(r'^api/(?P<resource>\w+)[/]?$', 'app.views.api_router', name='api'),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
