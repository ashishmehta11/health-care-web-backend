from   .models import Citizen
from rest_framework import serializers
class CitizenSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self,object):
        return object.user.email
    class Meta:
        model = Citizen
        fields = '__all__'