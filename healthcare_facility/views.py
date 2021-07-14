from django.conf import settings
from healthcare_facility.models import Affiliation, Facility, FacilityAffiliation
from django.contrib.auth.models import User     
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def facility_list(request):
   
    return HttpResponse("<h1> Hello there!</h1>")