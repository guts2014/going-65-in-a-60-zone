from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'bloomberg.views.main'),
    url(r'^status/', 'bloomberg.views.connection_status'),
    url(r'^sector/(?P<sector_type>\w+)/$', 'bloomberg.views.sector'),
    
    url(r'^chart/zoomable-circles', 'bloomberg.views.zoomablecircles'),
    url(r'^chart/zoomable-circles-json', 'bloomberg.views.json'),
    # url(r'^main/(?P<stock_num>\w+)/', 'bloomberg.views.main'),
)