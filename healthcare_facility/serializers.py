from rest_framework import serializers
from .models import Facility

class FacilitySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self,object):
        return object.user.email
    class Meta:
        model = Facility
        fields = '__all__'


