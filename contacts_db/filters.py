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

class NameFilter(InputFilter):
    parameter_name = 'name'
    title = 'name'    
    def queryset(self, request, queryset):
        term = self.value()        
        if term is None:
            return        
        any_name = Q()
        for bit in term.split():
            any_name &= (
                Q(first_name__icontains=bit) | 
                Q(last_name__icontains=bit) |
                Q(nickname__icontains=bit)
            )        
        return queryset.filter(any_name)

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
                Q(businesses__business__icontains=bit)
            )        
        return queryset.filter(any_name)

class PersonNameFilter(InputFilter):
    parameter_name = 'name'
    title = 'contact name'    
    def queryset(self, request, queryset):
        term = self.value()        
        if term is None:
            return        
        any_name = Q()
        for bit in term.split():
            any_name &= (
                Q(contacts__first_name__icontains=bit) | 
                Q(contacts__last_name__icontains=bit) |
                Q(contacts__nickname__icontains=bit)
            )        
        return queryset.filter(any_name).distinct()

class BusinessNameFilter(InputFilter):
    parameter_name = 'business'
    title = 'business name'    
    def queryset(self, request, queryset):
        term = self.value()
        if term is None:
            return        
        any_name = Q()
        for bit in term.split():
            any_name &= (
                Q(business__icontains=bit)
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
                Q(emails__email__icontains=bit)
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
                Q(socials__socialmedia__icontains=bit)
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
                Q(phones__phonenumber__icontains=bit)
            )        
        return queryset.filter(any_name).distinct()