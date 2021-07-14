from json.encoder import JSONEncoder
from django.http.response import JsonResponse
from rest_framework import generics, mixins, status
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.conf import settings
from healthcare_facility.models import Affiliation, Facility, FacilityAffiliation, FacilityOwnership, FacilitySpeciality, Ownership, Speciality
from django.contrib.auth.models import Group, User     
from django.shortcuts import render
from django.http import HttpResponse
from .serializers import FacilitySerializer


def get_dict(facility):
    facility_affiliations = FacilityAffiliation.objects.filter(facility=facility)
    facility_ownership = FacilityOwnership.objects.get(facility=facility)
    facility_speciality = FacilitySpeciality.objects.filter(facility=facility)
    d = {
        'id':facility.id,
        'user_name' : facility.user.email,
        'name' : facility.name,
        'address' : facility.address,
        'about' : facility.about,
        'established_date': facility.established_date,
        'city' : facility.city,
        'state' : facility.state,
        'pin_code': facility.pin_code,
        'contact_numbers' : facility.contact_numbers,
        'emails' : facility.emails,
        'avg_fees' :  facility.avg_fees
    }
    l =[]
    for i in facility_affiliations:
        l.append(i.affiliations.name)
    d.update({"affiliations" : l})
    d.update({
        "ownership":{
            'id' : facility_ownership.ownership.name,
            'name' : facility_ownership.name
        }
    })

    l = []

    for i in facility_speciality:
        l.append(i.speciality.name)
    
    d.update({'speciality' : l})

    return d
        


class FacilityListView(generics.GenericAPIView,mixins.ListModelMixin):
    serializer_class = FacilitySerializer

    def get(self,request):
        l =[]
        for facility in Facility.objects.all():
            l.append(get_dict(facility))
            
        d = {'facilities' : l}
        return JsonResponse(d,safe=False,status=200)

        
class FacilityDetailViewById(generics.RetrieveAPIView):
    serializer_class = FacilitySerializer

    def get(self,request,id):
        try:
            facility = Facility.objects.get(id=id)
            return JsonResponse(get_dict(facility),safe=False,status=200)
        except Facility.DoesNotExist:
            return JsonResponse({'error':'does not exists'},safe=False,status=404)


    

class FacilityDetailViewByCity(generics.ListAPIView):
    serializer_class = FacilitySerializer

    def get(self,request,state,city):
        try:
            facility = Facility.objects.get(state=state,city=city)
            return JsonResponse(get_dict(facility),safe=False,status=200)
        except Facility.DoesNotExist:
            return JsonResponse({'error':'does not exists'},safe=False,status=404)
        

class FacilityDetailViewByState(generics.ListAPIView):
    serializer_class = FacilitySerializer

    def get(self,request,state):
        try:
            facility = Facility.objects.get(state=state)
            return JsonResponse(get_dict(facility),safe=False,status=200)
        except Facility.DoesNotExist:
            return JsonResponse({'error':'does not exists'},safe=False,status=404)

class FacilityCreateView(generics.GenericAPIView,mixins.CreateModelMixin):
    serializer_class = FacilitySerializer
    def post(self,request):
        data = JSONParser().parse(request)
        try:
            User.objects.get(username=data['user_name'])
            d = {
                "error":"User already exists"
            }
            return JsonResponse(d,safe=False,status=400)
        except User.DoesNotExist:
            user = User.objects.create_user(data['user_name'],data['user_name'],data['password'])
            group = Group.objects.get(name='healthcare facility')
            group.user_set.add(user)

            facility = Facility(user=user,
            name=data['name'],
            address=data['address'],
            city=data['city'],
            state=data['state'],
            pin_code=data['pin_code'],
            about=data['about'],
            established_date=data['established_date'],
            contact_numbers=data['contact_numbers'],
            emails=data['emails'],
            avg_fees=data['avg_fees'])
            facility.save()

            l = data['affiliations']

            for i in l:
                affiliations = Affiliation.objects.get(name=i)
                facility_affiliations = FacilityAffiliation(facility=facility,affiliations=affiliations)
                facility_affiliations.save()

           

            l = data['speciality']

            for i in l:
                speciality = Speciality.objects.get(name=i)
                facility_speciality = FacilitySpeciality(facility=facility,speciality=speciality)
                facility_speciality.save()

            l = data['ownership']
            own = Ownership.objects.get(name=l['id'])
            facility_ownership = FacilityOwnership(facility=facility,ownership=own,name=l['name'])
            facility_ownership.save()

            res ={
                "success":"Facility Created Successfully"
            }
            return JsonResponse(res,safe=False,status=200)
        