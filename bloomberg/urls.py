from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'bloomberg.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       # url(r'^admin/', include(admin.site.urls)),

                       url(r'^status/', 'bloomberg.views.connection_status'),
                       url(r'^main/', 'bloomberg.views.main'),
                       url(r'^sector/(?P<sector>)', 'bloomberg.views.sector'),
                       # url(r'^main/(?P<stock_num>\w+)/', 'bloomberg.views.main'),
)
