
from django.conf.urls import url
from django.urls import path
from django.urls.conf import re_path
from .views import *

urlpatterns = [
    re_path(r'^facility/(?P<pk>[0-9]+)$', FacilityDetailViewById.as_view(),name="facility-detail-id"),
    re_path(r'^facility/(?P<state>[a-zA-Z_]+)/(?P<city>[a-zA-Z_]+)$', FacilityDetailViewByCity.as_view(),name="facility-list-by-city"),
    path('facility', FacilityListView.as_view(),name="facility-list"),
]
