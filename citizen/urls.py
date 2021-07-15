
from django.urls import path
from django.urls.conf import re_path
from .views import *

urlpatterns = [
    path('citizen-create', CitizenCreateView.as_view(),name="citizen-create"),
    path('citizen-update', CitizenUpdateView.as_view(),name="citizen-update"),
    path('citizen', CitizenDetailView.as_view(),name="citizen-detail-by-id")
]
