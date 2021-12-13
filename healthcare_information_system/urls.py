
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from .views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include(('healthcare_facility.urls','facility'),namespace='facility'),name="facility"),
    path('api/',include(('citizen.urls','citizen'),namespace='citizen'),name="citizen"),
    path('api/login', LoginView.as_view(),name="login"),
    path('api/delete', UserDeleteView.as_view(),name="user-delete"),
    path('api/logout', Logout.as_view(),name="logout"),
]
