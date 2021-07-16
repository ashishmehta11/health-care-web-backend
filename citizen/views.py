from healthcare_facility.models import Facility
from django.http.response import JsonResponse
from rest_framework import generics, mixins
from rest_framework.authtoken.models import Token
from rest_framework.parsers import JSONParser
from django.conf import settings
from django.contrib.auth.models import Group, User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Citizen
from .serializers import CitizenSerializer

# Create your views here.


class CitizenUpdateView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CitizenSerializer

    def post(self, request):
        tk = str(request.headers['Authorization']).split(' ')[1]
        data = JSONParser().parse(request)
        try:
            token = Token.objects.get(key=tk)
            user = User.objects.get(username=token.user.username)
            citizen = Citizen.objects.get(user=user)
            user = User.objects.get(username=data['user_name'])
            user.set_password(data['password'])
            if citizen.phone_number != data['phone_number']:
                try:
                    Facility.objects.get(contact_numbers__contains=str(
                        data['phone_number']))
                    d = {
                        "error": "Primary phone number already taken"
                    }
                    return JsonResponse(d, safe=False, status=403)
                except Facility.DoesNotExist:
                    try:
                        Citizen.objects.get(phone_number__contains=str(
                            data['phone_number']))
                        d = {
                            "error": "Primary phone number already taken"
                        }
                        return JsonResponse(d, safe=False, status=403)
                    except Citizen.DoesNotExist:
                        citizen.phone_number = data['phone_number']
            citizen.name = data['name']
            user.save()
            citizen.save()
            res = {
                "success": "Account Updated Successfully"
            }
            return JsonResponse(res, safe=False, status=201)

        except Citizen.DoesNotExist:
            d = {
                "error": "User does not already exists"
            }
            return JsonResponse(d, safe=False, status=404)
        except User.DoesNotExist:
            d = {
                "error": "User does not already exists"
            }
            return JsonResponse(d, safe=False, status=404)


class CitizenDetailView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CitizenSerializer

    def get(self, request):
        tk = str(request.headers['Authorization']).split(' ')[1]
        try:
            token = Token.objects.get(key=tk)
            user = User.objects.get(username=token.user.username)
            citizen = Citizen.objects.get(user=user)
            res = {
                'id': citizen.id,
                'user_name': citizen.user.username,
                'name': citizen.name,
                'phone_number': citizen.phone_number
            }
            return JsonResponse(res, safe=False, status=200)
        except Citizen.DoesNotExist:
            res = {
                'error': 'citizen does not exist'
            }
            return JsonResponse(res, safe=False, status=404)


class CitizenCreateView(generics.GenericAPIView):
    serializer_class = CitizenSerializer

    def post(self, request):
        data = JSONParser().parse(request)
        try:
            Citizen.objects.get(phone_number=data['phone_number'])
            d = {
                "error": "Phone number already taken"
            }
            print(d)
            return JsonResponse(d, safe=True, status=403)
        except Citizen.DoesNotExist:
            try:
                Facility.objects.get(contact_numbers__contains=str(
                data['phone_number']))
                d = {
                        "error": "Primary phone number already taken"
                    }
                return JsonResponse(d, safe=False, status=403)
            except Facility.DoesNotExist:
                try:
                    User.objects.get(username=data['user_name'])
                    d = {
                        "error": "Email already exists"
                    }
                    print(d)
                    return JsonResponse(d, safe=False, status=403)
                except User.DoesNotExist:
                    user = User.objects.create_user(
                        data['user_name'], data['user_name'], data['password'])
                    group = Group.objects.get(name='citizen')
                    group.user_set.add(user)

                    citizen = Citizen(
                        user=user, name=data["name"], phone_number=data['phone_number'])
                    citizen.save()
                    res = {
                        "success": "Account Created Successfully"
                    }
                    print(res)
                    return JsonResponse(res, safe=False, status=201)
