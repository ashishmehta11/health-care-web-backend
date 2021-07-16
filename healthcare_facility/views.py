from citizen.models import Citizen
from django.contrib.auth import models
from rest_framework import generics, mixins
from django.conf import settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from healthcare_facility.models import Affiliation, Facility, FacilityAffiliation, FacilityOwnership, FacilitySpeciality, Ownership, Speciality
from django.shortcuts import render
from .serializers import FacilitySerializer
from dateutil.parser import parse
from django.contrib.auth.models import Group, User
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse


def get_dict(facility):
    facility_affiliations = FacilityAffiliation.objects.filter(
        facility=facility)
    facility_ownership = FacilityOwnership.objects.get(facility=facility)
    facility_speciality = FacilitySpeciality.objects.filter(facility=facility)
    if facility.emails != None and len(facility.emails) > 0:
        d = {
            'id': facility.id,
            'user_name': facility.user.email,
            'name': facility.name,
            'address': facility.address,
            'about': facility.about,
            'established_date': facility.established_date,
            'city': facility.city,
            'state': facility.state,
            'pin_code': facility.pin_code,
            'contact_numbers': facility.contact_numbers,
            'emails': facility.emails,
            'avg_fees':  facility.avg_fees
        }
    else:
        d = {
            'id': facility.id,
            'user_name': facility.user.email,
            'name': facility.name,
            'address': facility.address,
            'about': facility.about,
            'established_date': facility.established_date,
            'city': facility.city,
            'state': facility.state,
            'pin_code': facility.pin_code,
            'contact_numbers': facility.contact_numbers,
            'avg_fees':  facility.avg_fees
        }
    l = []
    for i in facility_affiliations:
        l.append(i.affiliations.name)
    d.update({"affiliations": l})
    d.update({
        "ownership": {
            'id': facility_ownership.ownership.name,
            'name': facility_ownership.name
        }
    })

    l = []

    for i in facility_speciality:
        l.append(i.speciality.name)

    d.update({'speciality': l})

    return d


class FacilitySearch(generics.GenericAPIView):

    def post(self, request):
        data = JSONParser().parse(request)
        # address
        # affilations
        # speciality
        # ownership
        # name
        # avg fees

        address = ""
        affiliation = []
        speciality = []
        ownership = []
        name = ""
        avg_fees = ""

        if data.get('address') is not None:
            address = data['address']
        if data.get('name') is not None:
            name = data['mame']
        if data.get('affiliations') is not None:
            affiliation = data['affiliations']
        if data.get('speciality') is not None:
            speciality = data['speciality']
        if data.get('ownership') is not None:
            ownership = data['ownership']
        if data.get('avg_fees') is not None:
            avg_fees = data['avg_fees']

        if data.get('address') != None and data.get('affiliations') != None and data.get('speciality') != None and data.get('ownership') != None and data.get('name') != None and data.get('ownership') != None:
            try:
                l = []
                by_affiliated = []
                for a in affiliation:
                    for fa in FacilityAffiliation.objects.filter(affiliations=Affiliation.objects.get(name=a)):
                        by_affiliated.append(fa.facility)

                by_specials = []
                for a in speciality:
                    for fa in FacilitySpeciality.objects.filter(speciality=Speciality.objects.get(name=a)):
                        by_specials.append(fa.facility)

                by_owners = []
                for fa in FacilityOwnership.objects.filter(ownership=Ownership.objects.get(ownership=ownership)):
                    by_owners.append(fa.facility)

                by_adress = []
                for fa in FacilityOwnership.objects.filter(ownership=Ownership.objects.get(ownership=ownership)):
                    by_owners.append(fa.facility)

                res = {
                    "facilities": l
                }
                return JsonResponse(res, safe=False, status=200)
            except models.Model.DoesNotExist as e:
                print(e)
                res = {
                    "error": "no result found"
                }
                return JsonResponse(res, safe=False, status=404)


class FacilityUpdateView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        tk = str(request.headers['Authorization']).split(' ')[1]
        data = JSONParser().parse(request)
        try:
            try:
                Facility.objects.get(contact_numbers__contains=str(data['contact_numbers']).split(';')[0])
                d = {
                    "error": "Primary phone number already taken"
                }
                return JsonResponse(d, safe=False, status=403)
            except Facility.DoesNotExist:
                try:
                    Citizen.objects.get(phone_number__contains=str(data['contact_numbers']).split(';')[0])
                    d = {
                        "error": "Primary phone number already taken"
                    }
                    return JsonResponse(d, safe=False, status=403)
                except Citizen.DoesNotExist:
                    token = Token.objects.get(key=tk)
                    print('token belongs to ', token.user.username)
                    user = User.objects.get(username=token.user.username)
                    facility = Facility.objects.get(user=user)
                    if data.get('password', None) != None:
                        user.set_password(data['password'])
                    print('facility belongs to ', facility.user.username)
                    print('facility id ', facility.id)
                    print('user belongs to ', user.username)
                    if data.get('emails') is None or data.get('emails', 'null') == 'null':
                        facility.emails = None
                    else:
                        facility.emails = data['emails']
                    facility.name = data['name']
                    facility.address = data['address']
                    facility.city = data['city']
                    facility.state = data['state']
                    facility.pin_code = data['pin_code']
                    facility.contact_numbers = data['contact_numbers']
                    facility.about = data['about']
                    facility.established_date = parse(data['established_date'])

                    for f_a in FacilityAffiliation.objects.filter(facility=facility):
                        f_a.delete()

                    for f_s in FacilitySpeciality.objects.filter(facility=facility):
                        f_s.delete()

                    for f_w in FacilityOwnership.objects.filter(facility=facility):
                        f_w.delete()

                    l = data['affiliations']

                    for i in l:
                        affiliations = Affiliation.objects.get(name=i)
                        facility_affiliations = FacilityAffiliation(
                            facility=facility, affiliations=affiliations)
                        facility_affiliations.save()

                    l = data['speciality']

                    for i in l:
                        speciality = Speciality.objects.get(name=i)
                        facility_speciality = FacilitySpeciality(
                            facility=facility, speciality=speciality)
                        facility_speciality.save()

                    l = data['ownership']
                    own = Ownership.objects.get(name=l['id'])
                    facility_ownership = FacilityOwnership(
                        facility=facility, ownership=own, name=l['name'])
                    facility_ownership.save()

                    user.save()
                    facility.save()
                    res = {
                        "success": "Account Updated Successfully"
                    }

                    return JsonResponse(res, safe=False, status=200)

        except Facility.DoesNotExist:
            d = {
                "error": "User does not already exists"
            }
            return JsonResponse(d, safe=False, status=404)
        except User.DoesNotExist:
            d = {
                "error": "User does not already exists"
            }
            return JsonResponse(d, safe=False, status=404)


class FacilityListView(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = FacilitySerializer

    def get(self, request):
        l = []
        for facility in Facility.objects.all():
            l.append(get_dict(facility))

        d = {'facilities': l}
        return JsonResponse(d, safe=False, status=200)


class FacilityDetailViewById(generics.RetrieveAPIView):
    serializer_class = FacilitySerializer

    def get(self, request, id):
        try:
            facility = Facility.objects.get(id=id)
            return JsonResponse(get_dict(facility), safe=False, status=200)
        except Facility.DoesNotExist:
            return JsonResponse({'error': 'not found'}, safe=False, status=404)


class FacilityDetailViewByCity(generics.ListAPIView):
    serializer_class = FacilitySerializer

    def get(self, request, state, city):
        try:
            l = []
            state = str(state).replace('_', ' ')
            city = str(city).replace('_', ' ')
            for facility in Facility.objects.filter(state=state, city=city):
                l.append(get_dict(facility))

            d = {'facilities': l}
            return JsonResponse(d, safe=False, status=200)
        except Facility.DoesNotExist:
            return JsonResponse({'error': 'not found'}, safe=False, status=404)


class FacilityDetailViewByState(generics.ListAPIView):
    serializer_class = FacilitySerializer

    def get(self, request, state):
        try:
            l = []
            state = str(state).replace('_', ' ')
            for facility in Facility.objects.filter(state=state):
                l.append(get_dict(facility))

            d = {'facilities': l}
            return JsonResponse(d, safe=False, status=200)
        except Facility.DoesNotExist:
            return JsonResponse({'error': 'not found'}, safe=False, status=404)


class FacilityCreateView(generics.GenericAPIView, mixins.CreateModelMixin):
    serializer_class = FacilitySerializer

    def post(self, request):
        data = JSONParser().parse(request)
        try:
            User.objects.get(username=data['user_name'])
            d = {
                "error": "User already exists"
            }
            return JsonResponse(d, safe=False, status=403)
        except User.DoesNotExist:
            try:
                Facility.objects.get(contact_numbers__contains=str(data['contact_numbers']).split(';')[0])
                d = {
                    "error": "Primary phone number already taken"
                }
                return JsonResponse(d, safe=False, status=403)
            except Facility.DoesNotExist:
                try:
                    Citizen.objects.get(phone_number__contains=str(data['contact_numbers']).split(';')[0])
                    d = {
                        "error": "Primary phone number already taken"
                    }
                    return JsonResponse(d, safe=False, status=403)
                except Citizen.DoesNotExist:
                    group = Group.objects.get(name='healthcare facility')
                    user = User.objects.create_user(
                        data['user_name'], data['user_name'], data['password'])
                    group.user_set.add(user)
                    datetime_obj = parse(data['established_date'])
                    if data.get('emails') is None or data.get('emails', 'null') == 'null':
                        facility = Facility(user=user,
                                            name=data['name'],
                                            address=data['address'],
                                            city=data['city'],
                                            state=data['state'],
                                            pin_code=data['pin_code'],
                                            about=data['about'],
                                            established_date=datetime_obj,
                                            contact_numbers=data['contact_numbers'],
                                            avg_fees=data['avg_fees'])

                    else:
                        facility = Facility(user=user,
                                            name=data['name'],
                                            address=data['address'],
                                            city=data['city'],
                                            state=data['state'],
                                            pin_code=data['pin_code'],
                                            about=data['about'],
                                            established_date=datetime_obj,
                                            contact_numbers=data['contact_numbers'],
                                            emails=data['emails'],
                                            avg_fees=data['avg_fees'])

                    facility.save()

                    l = data['affiliations']

                    for i in l:
                        affiliations = Affiliation.objects.get(name=i)
                        facility_affiliations = FacilityAffiliation(
                            facility=facility, affiliations=affiliations)
                        facility_affiliations.save()

                    l = data['speciality']

                    for i in l:
                        speciality = Speciality.objects.get(name=i)
                        facility_speciality = FacilitySpeciality(
                            facility=facility, speciality=speciality)
                        facility_speciality.save()

                    l = data['ownership']
                    own = Ownership.objects.get(name=l['id'])
                    facility_ownership = FacilityOwnership(
                        facility=facility, ownership=own, name=l['name'])
                    facility_ownership.save()

                    res = {
                        "success": "Facility Created Successfully"
                    }
                    return JsonResponse(res, safe=False, status=201)
