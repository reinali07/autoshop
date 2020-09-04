from django.db.models import Q
from django.contrib import admin
from django.contrib.admin.views.main import ChangeList

class InputFilter(admin.SimpleListFilter):
    template = 'admin/input_filter.html'

    def lookups(self, request, model_admin):
        # Dummy, required to show the filter.
        return ((),)

    def choices(self, changelist):
        # Grab only the "all" option.
        all_choice = next(super().choices(changelist))
        all_choice['query_parts'] = (
            (k, v)
            for k, v in changelist.get_filters_params().items()
            if k != self.parameter_name
        )
        yield all_choice

class VINFilter(InputFilter):
    parameter_name = 'vin'
    title = 'VIN'    
    def queryset(self, request, queryset):
        term = self.value()        
        if term is None:
            return        
        any_name = Q()
        for bit in term.split():
            any_name &= (
                Q(vin__icontains=bit)
            )        
        return queryset.filter(any_name).distinct()

class LicenseFilter(InputFilter):
    parameter_name = 'licenseplate'
    title = 'license plate'    
    def queryset(self, request, queryset):
        term = self.value()        
        if term is None:
            return        
        any_name = Q()
        for bit in term.split():
            any_name &= (
                Q(licenseplate__icontains=bit)
            )        
        return queryset.filter(any_name).distinct()
        
class ColourFilter(InputFilter):
    parameter_name = 'colour'
    title = 'colour'
    def queryset(self, request, queryset):
        term = self.value()        
        if term is None:
            return        
        any_name = Q()
        for bit in term.split():
            any_name &= (
                Q(colour__icontains=bit)
            )        
        return queryset.filter(any_name).distinct()

class MakeModelFilter(InputFilter):
    parameter_name = 'makemodel'
    title = 'make and model'    
    def queryset(self, request, queryset):
        term = self.value()
        if term is None:
            return        
        any_name = Q()
        for bit in term.split():
            any_name &= (
                #Q(vehicle_makemodel__make__icontains=bit) |
                #Q(vehicle_makemodel__vehiclemodel__icontains=bit) |
                Q(clientvehicle__vehicle_makemodel__makemodel__icontains=bit)
            )        
        return queryset.filter(any_name).distinct()

class CommentFilter(InputFilter):
    parameter_name = 'comment'
    title = 'comments'
    def queryset(self, request, queryset):
        term = self.value()
        if term is None:
            return        
        any_name = Q()
        for bit in term.split():
            any_name &= (
                Q(clientvehicle__brake_note__icontains=bit) |
                Q(clientcontact__comments__icontains=bit)
            )        
        return queryset.filter(any_name).distinct()

class PersonNameFilter(InputFilter):
    parameter_name = 'name'
    title = 'name'    
    def queryset(self, request, queryset):
        term = self.value()        
        if term is None:
            return        
        any_name = Q()
        for bit in term.split():
            any_name &= (
                Q(clientcontact__first_name__icontains=bit) | 
                Q(clientcontact__last_name__icontains=bit) |
                Q(clientcontact__nickname__icontains=bit)
            )        
        return queryset.filter(any_name).distinct()

class BusinessFilter(InputFilter):
    parameter_name = 'business'
    title = 'business'    
    def queryset(self, request, queryset):
        term = self.value()
        if term is None:
            return        
        any_name = Q()
        for bit in term.split():
            any_name &= (
                Q(clientcontact__businesses__business__icontains=bit)
            )        
        return queryset.filter(any_name).distinct()

class EmailFilter(InputFilter):
    parameter_name = 'email'
    title = 'email'    
    def queryset(self, request, queryset):
        term = self.value()
        if term is None:
            return        
        any_name = Q()
        for bit in term.split():
            any_name &= (
                Q(clientcontact__emails__email__icontains=bit)
            )        
        return queryset.filter(any_name).distinct()

class SocialFilter(InputFilter):
    parameter_name = 'social'
    title = 'social media'    
    def queryset(self, request, queryset):
        term = self.value()
        if term is None:
            return        
        any_name = Q()
        for bit in term.split():
            any_name &= (
                Q(clientcontact__socials__socialmedia__icontains=bit)
            )        
        return queryset.filter(any_name).distinct()

class PhoneFilter(InputFilter):
    parameter_name = 'phone_number'
    title = 'phone number'    
    def queryset(self, request, queryset):
        term = self.value()        
        if term is None:
            return        
        any_name = Q()
        for bit in term.split():
            any_name &= (
                Q(clientcontact__phones__phonenumber__icontains=bit)
            )        
        return queryset.filter(any_name).distinct()