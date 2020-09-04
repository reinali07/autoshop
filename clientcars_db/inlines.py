import contacts_db.models as contact_models
import vehicles_db.models as vehicle_models
from django.contrib import admin
from .models import *
from vehicles_db.models import Vehicle
'''
class ContactInline(admin.TabularInline):
    model = Client.clientcontact.through
    extra = 1
    autocomplete = ('contact',)
'''
class VehicleInline(admin.TabularInline):
    model = Vehicle
    extra = 1
    autocomplete = ('vehicle_makemodel')