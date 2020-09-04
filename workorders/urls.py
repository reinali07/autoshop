from django.urls import path,include
from . import views
from dal import autocomplete
from .models import *

app_name = 'workorders'
urlpatterns = [
    path('pdf/',views.GeneratePdf.as_view(),name='pdf'),
    path('get_defaults/',views.get_defaults,name='get_defaults')
]