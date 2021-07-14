from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Facility)
admin.site.register(Affiliation)
admin.site.register(FacilityAffiliation)
admin.site.register(Ownership)
admin.site.register(FacilityOwnership)
admin.site.register(FacilitySpeciality)
admin.site.register(Speciality)