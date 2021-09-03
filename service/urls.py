# -*- coding: utf-8 -*-

from mg.satellite import views
from share.utils import custom_url as url

satellite_urlpatterns = [

    url(r'^satellite/event_list/$', views.SatelliteListView.as_view(), name='satellite_list'),

    url(r'^satellite/create_event/$', views.SatelliteCreateView.as_view(), name='create_satellite'),

    url(r'^satellite/query_group/$', views.QueryGroupView.as_view(), name='query_group'),

]
