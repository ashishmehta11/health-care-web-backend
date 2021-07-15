from django.db import models
from django.db.models.deletion import CASCADE
from django.conf import settings

# Create your models here.

class Citizen(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=CASCADE)
    name = models.TextField(null=False,blank=False)
    phone_number = models.TextField(null=False,blank=False,unique=True)


def __str__(self):
        return f"({self.id})\n{self.name}\n{self.phone_number}"