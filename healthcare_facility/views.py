from rest_framework import generics
from django.conf import settings
from healthcare_facility.models import Affiliation, Facility, FacilityAffiliation
from django.contrib.auth.models import User     
from django.shortcuts import render
from django.http import HttpResponse
from .serializers import FacilitySerializer


class FacilityListView(generics.ListAPIView):

    serializer_class = FacilitySerializer

    def get_queryset(self):
        return Facility.objects.all()

        
class FacilityDetailViewById(generics.RetrieveAPIView):
    lookup_field = 'pk' #r'?P<id>\d+'
    serializer_class = FacilitySerializer

    def get_queryset(self):
        return Facility.objects.all()


    

class FacilityDetailViewByCity(generics.ListAPIView):
    serializer_class = FacilitySerializer

    def get_queryset(self):
        state = self.kwargs.get('state')
        state = str(state).replace('_',' ')
        city = self.kwargs.get('city')
        city= str(city).replace('_',' ')
        return Facility.objects.filter(state=state,city=city)
        

