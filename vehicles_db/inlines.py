from django.contrib import admin
from .models import *
from clientcars_db import models as client_models

class ClientInline(admin.TabularInline):
    verbose_name_plural = "Car and Owners"
    model = client_models.Client
    extra = 1
    #autocomplete_fields = ('vehicle__vehicle_makemodel__makemodel')


'''
class YearInline(admin.TabularInline):
    model = Vehicle.vehicle_year.through
    extra = 1
    max_num = 1
    can_delete = False
    autocomplete_fields = ('year',)
'''
'''
class MakeInline(admin.TabularInline):
    model = Vehicle.vehicle_make.through
    extra = 1
    max_num = 1
    can_delete = False
    autocomplete_fields = ('make',)
'''
'''
class MakeModelInline(admin.TabularInline):
    verbose_name_plural = "Make and Model"
    verbose_name = "Make and Model"
    model = Vehicle.vehicle_makemodel.through
    extra = 1
    max_num = 1
    can_delete = False
    autocomplete_fields = ('makemodel',)
'''
'''
class VehicleModelInline(admin.TabularInline):
    model = Vehicle.vehicle_vehiclemodel.through
    extra = 1
    max_num = 1
    can_delete = False
    autocomplete_fields = ('vehiclemodel',)
'''
#class TrimInline(admin.TabularInline):
#    model = Trim
#    can_delete = False
#    autocomplete_fields = ('trim',)
'''
class TrimInline(admin.TabularInline):
    verbose_name_plural = "Trim"
    model = Vehicle.vehicle_trim.through
    extra = 1
    max_num = 1
    can_delete = False
    autocomplete_fields = ('trim',)

class EngineSizeInline(admin.TabularInline):
    verbose_name_plural = "Engine Size"
    model = Vehicle.vehicle_enginesize.through
    extra = 1
    max_num = 1
    can_delete = False
    autocomplete_fields = ('enginesize',)

class EngineCodeInline(admin.TabularInline):
    verbose_name_plural = "Engine Code"
    model = Vehicle.vehicle_enginecode.through
    extra = 1
    max_num = 1
    can_delete = False
    autocomplete_fields = ('enginecode',)
    '''