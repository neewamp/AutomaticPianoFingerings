from django.conf.urls import include, url
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

import hello.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^manual', hello.views.manual, name='manual'),
    url(r'^history', hello.views.history, name='history'),
    url(r'^$', hello.views.index, name='index'),
    url(r'^db', hello.views.db, name='db'),
    url(r'^admin/', admin.site.urls),
    url(r'^weekone/first/', hello.views.first, name='first'),
    url(r'^weekone/', hello.views.weekone, name='weekone'),
    url(r'^presentation/', hello.views.pres, name='pres'),
    url(r'^upload/', hello.views.upload, name='upload'),
    url(r'^test/', hello.views.test, name='test'),
] + static('annotated/', document_root='annotated/')

