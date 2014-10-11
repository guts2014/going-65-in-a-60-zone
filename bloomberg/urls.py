from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'bloomberg.views.main'),
    url(r'^status/', 'bloomberg.views.connection_status'),
    url(r'^sector/(?P<sector_type>\w+)/$', 'bloomberg.views.sector'),
    
    url(r'^chart/history', 'bloomberg.chart.history'),
    
    url(r'^chart/zoomcircles', 'bloomberg.chart.zoom_circles_page'),
    url(r'^data/zoomcircles', 'bloomberg.chart.zoom_circles_data'),
    # url(r'^main/(?P<stock_num>\w+)/', 'bloomberg.views.main'),
)
