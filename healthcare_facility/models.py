from django.db import models
from django.db.models import fields, indexes
from django.db.models.deletion import CASCADE
from django.conf import UserSettingsHolder, settings

# Create your models here.
class Facility(models.Model):

    user = models.ForeignKey( settings.AUTH_USER_MODEL,on_delete=CASCADE)
    name = models.TextField(null=True,blank=True)
    address = models.TextField(null=False,blank=False)
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
        return f"{self.name}"


class FacilityAffiliation(models.Model):
    facility = models.ForeignKey(Facility,on_delete=CASCADE)
    affiliations = models.ForeignKey(Affiliation,on_delete=CASCADE)

    class Meta:
        # indexes =[
        #     models.Index(fields = ['facility','affiliations']),
        # ]

        unique_together = (('facility','affiliations'))

class Ownership(models.Model):
    name = models.TextField(null=False,blank=False,unique=True)

class FacilityOwnership(models.Model):
    facility = models.ForeignKey(Facility,on_delete=CASCADE)
    ownership = models.ForeignKey(Ownership,on_delete=CASCADE)

    class Meta:
        # indexes = [
        #     models.Index(fields=['facility','ownership'])
        # ]

         unique_together = (('facility','ownership'))
