
from django.urls import path
from django.urls.conf import re_path
from .views import *

urlpatterns = [
    path('facility/affiliations/<str:affiliations>', FacilityByAffiliations.as_view(),name="facility-by-affiliations"),
    path('facility/<int:id>', FacilityDetailViewById.as_view(),name="facility-detail-by-id"),
    path('facility/<str:state>/<str:city>', FacilityDetailViewByCity.as_view(),name="facility-list-by-city"),
    path('facility/<str:state>', FacilityDetailViewByState.as_view(),name="facility-list-by-state"),
    path('facility', FacilityListView.as_view(),name="facility-list"),
    path('facility-create', FacilityCreateView.as_view(),name="facility-create"),
    path('facility-update', FacilityUpdateView.as_view(),name="facility-update"),
    
]
