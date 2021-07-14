from django.db import models
from django.db.models import fields, indexes
from django.db.models.deletion import CASCADE
from django.conf import UserSettingsHolder, settings

# Create your models here.
class Facility(models.Model):

    user= models.ForeignKey( settings.AUTH_USER_MODEL,on_delete=CASCADE)
    name = models.TextField(null=False,blank=False)
    address = models.TextField(null=False,blank=False)
    city = models.TextField(null=False,blank=False)
    state = models.TextField(null=False,blank=False)
    pin_code=models.IntegerField(null=False,blank=False)
    about = models.TextField(null=False,blank=False)
    established_date = models.DateTimeField(null=False,blank=False)
    contact_numbers = models.TextField(null=False,blank=False)
    emails = models.TextField(null=True,blank=False)
    avg_fees = models.FloatField(null=False,blank=False)

    def __str__(self):
        return f"({self.id})\n{self.name}"

class Affiliation(models.Model):
    name = models.TextField(null=False,blank=False,unique=True)

    def __str__(self):
        return f"({self.id})\n{self.name}"


class FacilityAffiliation(models.Model):
    facility = models.ForeignKey(Facility,on_delete=CASCADE)
    affiliations = models.ForeignKey(Affiliation,on_delete=CASCADE)

    class Meta:
        # indexes =[
        #     models.Index(fields = ['facility','affiliations']),
        # ]

        unique_together = (('facility','affiliations'))
        
    def __str__(self):
        return f"({self.id})\n{self.facility.name}\n{self.affiliations.name}"


class Ownership(models.Model):
    name = models.TextField(null=False,blank=False,unique=True)
    def __str__(self):
        return f"({self.id})\n{self.name}"

class FacilityOwnership(models.Model):
    facility = models.ForeignKey(Facility,on_delete=CASCADE)
    ownership = models.ForeignKey(Ownership,on_delete=CASCADE)
    name = models.TextField(null=False,blank=False)
    class Meta:
        # indexes = [
        #     models.Index(fields=['facility','ownership'])
        # ]

         unique_together = (('facility','ownership'))

    def __str__(self):
        return f"({self.id})\n{self.facility.name}\n{self.ownership.name}\n{self.name}"

class Speciality(models.Model):
    name = models.TextField(null=False,blank=False,unique=True)

    def __str__(self):
        return f"({self.id})\n{self.name}"

class FacilitySpeciality(models.Model):
    facility = models.ForeignKey(Facility,on_delete=CASCADE)
    speciality = models.ForeignKey(Speciality,on_delete=CASCADE)

    class Meta:
        # indexes = [
        #     models.Index(fields=['facility','ownership'])
        # ]

         unique_together = (('facility','speciality'))

    def __str__(self):
        return f"({self.id})\n{self.facility.name}\n{self.speciality.name}"
