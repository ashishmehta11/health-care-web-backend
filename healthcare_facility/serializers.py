from django.contrib.auth.models import User
from django.db.models import fields
from django.db.models.base import Model
from rest_framework import serializers
from rest_framework.utils import field_mapping, model_meta
from .models import Facility

class FacilitySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self,object):
        return object.user.email
    class Meta:
        model = Facility
        fields = '__all__'