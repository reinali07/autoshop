from django.contrib import admin
from django.utils.html import format_html
from .models import *
from .inlines import *
from .filters import *
from .forms import *

# Register your models here.

class VehicleAdmin(admin.ModelAdmin):
    inlines = [
        #YearInline,
        #MakeInline,
        #VehicleModelInline,
        #MakeModelInline,
        #TrimInline,
        #EngineSizeInline,
        #EngineCodeInline,
        #ClientInline
    ]
    search_fields = ['vehicle',]
    #exclude = ['vehicle_year','vehicle_make','vehicle_vehiclemodel','vehicle_trim','vehicle_enginesize','vehicle_enginecode']
    exclude = ['vehicle',]

    fieldsets = [
        (None, {
            'fields': [('year'),('vehicle_makemodel','vehicle_trim'),('vehicle_enginesize','vehicle_enginecode',),('transmission_type','drive_wheel','rear_brake_style','e_brake_style',), ('power_steering_type','absys','tpms','ac'),('tire_size_prefix','tire_size')]
        }),
        ('Brake Notes', {
            'fields': ['brake_note',],
        }),
        ('Notes/Comments', {
            'fields': ['comments',],
        }),
    ]
    autocomplete_fields = ('vehicle_makemodel','vehicle_trim','vehicle_enginesize','vehicle_enginecode',)
    def delete_vehicle(self, obj):
        return format_html('<a class="btn" href="/admin/vehicles_db/vehicle/{}/delete/">Delete</a>', obj.id)
    
    list_display = ['__str__','vehicle','delete_vehicle']
    #list_filter = [YearFilter,MakeFilter,VehicleModelFilter,TrimFilter,EngineSizeFilter,EngineCodeFilter]
    list_filter = [YearFilter,MakeModelFilter,TrimFilter,EngineSizeFilter,EngineCodeFilter]
'''
class YearAdmin(admin.ModelAdmin):
    search_fields = ['year']
    ordering = ['year']
    exclude = ['strid']
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}
'''
class MakeModelAdmin(admin.ModelAdmin):
    search_fields = ['makemodel',]
    ordering = ['makemodel',]
    exclude = ['makemodel',]
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}

'''
class VehicleModelAdmin(admin.ModelAdmin):
    search_fields = ['vehiclemodel']
    ordering = ['vehiclemodel']
    exclude = ['strid']
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}

class MakeAdmin(admin.ModelAdmin):
    search_fields = ['make']
    ordering = ['make']
    exclude = ['strid']
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}
'''

class TrimAdmin(admin.ModelAdmin):
    search_fields = ['trim']
    ordering = ['trim']
    #exclude = ['strid']
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}

class EngineSizeAdmin(admin.ModelAdmin):
    search_fields = ['enginesize']
    ordering = ['enginesize']
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}

class EngineCodeAdmin(admin.ModelAdmin):
    search_fields = ['enginecode']
    ordering = ['enginecode']
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}

admin.site.register(Vehicle,VehicleAdmin)
admin.site.register(MakeModel,MakeModelAdmin)
#admin.site.register(Year,YearAdmin)
#admin.site.register(Make,MakeAdmin)
#admin.site.register(VehicleModel,VehicleModelAdmin)
admin.site.register(Trim,TrimAdmin)
admin.site.register(EngineSize,EngineSizeAdmin)
admin.site.register(EngineCode,EngineCodeAdmin)
