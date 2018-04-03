from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import hello.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', hello.views.index, name='index'),
    url(r'^db', hello.views.db, name='db'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^weekone/first/', hello.views.first, name='first'),
    url(r'^weekone/', hello.views.weekone, name='weekone'),
    url(r'^presentation/', hello.views.pres, name='pres'),
    url(r'^upload/', hello.views.upload, name='upload'),
    url(r'^manual/', hello.views.manual, name='manual'),
]
