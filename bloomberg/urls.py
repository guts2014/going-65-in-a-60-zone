from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'bloomberg.views.main'),
    url(r'^status/', 'bloomberg.views.connection_status'),

    url(r'^chart/history', 'bloomberg.chart.history'),
    
    url(r'^chart/zoomcircles/uk', 'bloomberg.chart.zoom_circles_page', {"country": "uk"}),
    url(r'^data/zoomcircles/uk', 'bloomberg.chart.zoom_circles_data', {"country": "UK"}),
    
    url(r'^chart/zoomcircles/us', 'bloomberg.chart.zoom_circles_page', {"country": "us"}),
    url(r'^data/zoomcircles/us', 'bloomberg.chart.zoom_circles_data', {"country": "US"}),
	
	url(r'^sounds', 'bloomberg.sound.sounds_page'),
    # url(r'^main/(?P<stock_num>\w+)/', 'bloomberg.views.main'),
)
