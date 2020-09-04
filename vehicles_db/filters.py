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

'''
class YearFilter(InputFilter):
    parameter_name = 'year'
    title = 'year'    
    def queryset(self, request, queryset):
        term = self.value()        
        if term is None:
            return        
        any_name = Q()
        for bit in term.split():
            any_name &= (
                Q(vehicle_year__year__icontains=bit)
            )        
        return queryset.filter(any_name)
'''
class YearFilter(InputFilter):
    parameter_name = 'year'
    title = 'year'    
    def queryset(self, request, queryset):
        term = self.value()        
        if term is None:
            return        
        any_name = Q()
        for bit in term.split():
            any_name &= (
                Q(year__icontains=bit)
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
                Q(vehicle_makemodel__makemodel__icontains=bit)
            )        
        return queryset.filter(any_name).distinct()

'''
class MakeFilter(InputFilter):
    parameter_name = 'make'
    title = 'make'    
    def queryset(self, request, queryset):
        term = self.value()
        if term is None:
            return        
        any_name = Q()
        for bit in term.split():
            any_name &= (
                Q(vehicle_make__make__icontains=bit)
            )        
        return queryset.filter(any_name)

class VehicleModelFilter(InputFilter):
    parameter_name = 'vehiclemodel'
    title = 'model'    
    def queryset(self, request, queryset):
        term = self.value()
        if term is None:
            return        
        any_name = Q()
        for bit in term.split():
            any_name &= (
                Q(vehicle_vehiclemodel__vehiclemodel__icontains=bit)
            )        
        return queryset.filter(any_name)
'''

class TrimFilter(InputFilter):
    parameter_name = 'trim'
    title = 'trim'    
    def queryset(self, request, queryset):
        term = self.value()
        if term is None:
            return        
        any_name = Q()
        for bit in term.split():
            any_name &= (
                Q(vehicle_trim__trim__icontains=bit)
            )        
        return queryset.filter(any_name).distinct()

class EngineSizeFilter(InputFilter):
    parameter_name = 'enginesize'
    title = 'engine size'    
    def queryset(self, request, queryset):
        term = self.value()        
        if term is None:
            return        
        any_name = Q()
        for bit in term.split():
            any_name &= (
                Q(vehicle_enginesize__enginesize__icontains=bit)
            )        
        return queryset.filter(any_name).distinct()

class EngineCodeFilter(InputFilter):
    parameter_name = 'enginecode'
    title = 'engine code'    
    def queryset(self, request, queryset):
        term = self.value()        
        if term is None:
            return        
        any_name = Q()
        for bit in term.split():
            any_name &= (
                Q(vehicle_enginecode__enginecode__icontains=bit)
            )        
        return queryset.filter(any_name).distinct()