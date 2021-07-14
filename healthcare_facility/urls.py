
from django.urls import path
from .views import *

urlpatterns = [
    path('', facility_list),
]
