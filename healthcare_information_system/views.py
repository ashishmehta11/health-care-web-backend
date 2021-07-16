from django.contrib.auth import authenticate
from healthcare_facility.views import get_dict
from django.contrib.auth.models import Group, User
from django.http.response import JsonResponse
from rest_framework.authentication import TokenAuthentication

from rest_framework.authtoken.models import Token
from rest_framework import generics, mixins
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from citizen.models import Citizen
from healthcare_facility.models import Facility, FacilityAffiliation, FacilityOwnership, FacilitySpeciality


# def get_dict(facility):
#     facility_affiliations = FacilityAffiliation.objects.filter(facility=facility)
#     facility_ownership = FacilityOwnership.objects.get(facility=facility)
#     facility_speciality = FacilitySpeciality.objects.filter(facility=facility)
#     d = {
#         'id':facility.id,
#         'user_name' : facility.user.username,
#         'name' : facility.name,
#         'address' : facility.address,
#         'about' : facility.about,
#         'established_date': facility.established_date,
#         'city' : facility.city,
#         'state' : facility.state,
#         'pin_code': facility.pin_code,
#         'contact_numbers' : facility.contact_numbers,
#         'emails' : facility.emails,
#         'avg_fees' :  facility.avg_fees,
#     }
#     l =[]
#     for i in facility_affiliations:
#         l.append(i.affiliations.name)
#     d.update({"affiliations" : l})
#     d.update({
#         "ownership":{
#             'id' : facility_ownership.ownership.name,
#             'name' : facility_ownership.name
#         }
#     })

#     l = []

#     for i in facility_speciality:
#         l.append(i.speciality.name)

#     d.update({'speciality' : l})

#     return d


class LoginView(generics.GenericAPIView):
    def post(self, request):
        data = JSONParser().parse(request)
        try:
            res = {

            }
            user = authenticate(
                username=data['user_name'], password=data['password'])
            if user is None:
                res = {
                    "error": "Invalid user id or password"
                }
                return JsonResponse(res, safe=False, status=401)
            token, created = Token.objects.get_or_create(user=user)
            print("token = ", token.key)
            if user.groups.filter(name='citizen'):
                print("here!!1")
                citizen = Citizen.objects.get(user=user)
                res = {
                    "id": citizen.id,
                    "token": token.key,
                    'group': 'citizen',
                    'name': citizen.name,
                    'user_name': citizen.user.username,
                    'phone_number': citizen.phone_number,
                }
                return JsonResponse(res, safe=False, status=200)
            else:
                facility = Facility.objects.get(user=user)
                res = {
                    'group': 'healthcare facility',
                    'token': token.key,
                    'facility': get_dict(facility)
                }
                return JsonResponse(res, safe=False, status=200)
        except User.DoesNotExist:
            res = {
                "error": "Invalid user id or password"
            }
            return JsonResponse(res, safe=False, status=401)


class UserDeleteView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tk = str(request.headers['Authorization']).split(' ')[1]
        try:
            token = Token.objects.get(key=tk)
            user = User.objects.get(username=token.user.username)
            user.delete()
            res = {
                "success": "user deleted"
            }
            return JsonResponse(res, safe=False, status=200)
        except User.DoesNotExist:
            d = {
                "error": "User does not already exists"
            }
            return JsonResponse(d, safe=False, status=404)


class Logout(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        res = {
            "success": "logout successful"
        }
        try:
            tk = str(request.headers['Authorization']).split(' ')[1]
            token = Token.objects.get(key=tk)
            token.delete()
        except Token.DoesNotExist:
            pass
        finally:
            return JsonResponse(res, safe=False, status=200)
