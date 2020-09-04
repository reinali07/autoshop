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

class ReferenceFilter(InputFilter):
    parameter_name = 'invoice'
    title = 'invoice number'    
    def queryset(self, request, queryset):
        term = self.value()        
        if term is None:
            return        
        any_name = Q()
        for bit in term.split():
            any_name &= (
                Q(reference__icontains=bit) |
                Q(supplier_invoice__icontains=bit)
            )        
        return queryset.filter(any_name).distinct()

class POFilter(InputFilter):
    parameter_name = 'po'
    title = 'po'    
    def queryset(self, request, queryset):
        term = self.value()        
        if term is None:
            return        
        any_name = Q()
        for bit in term.split():
            any_name &= (
                Q(po__icontains=bit)
            )        
        return queryset.filter(any_name).distinct()

class PartFilter(InputFilter):
    parameter_name = 'part'
    title = 'part'    
    def queryset(self, request, queryset):
        term = self.value()        
        if term is None:
            return        
        any_name = Q()
        for bit in term.split():
            any_name &= (
                Q(purchased_parts__part__icontains=bit) |
                Q(purchased_parts__internal__part_number__icontains=bit)
            )        
        return queryset.filter(any_name).distinct()

class PricePartFilter(InputFilter):
    parameter_name = 'part'
    title = 'brand and part'    
    def queryset(self, request, queryset):
        term = self.value()        
        if term is None:
            return        
        any_name = Q()
        for bit in term.split():
            any_name &= (
                Q(part__part__icontains=bit) |
                Q(part__internal__part_number__icontains=bit)
            )        
        return queryset.filter(any_name).distinct()

class InvoiceFilter(InputFilter):
    parameter_name = 'invoice'
    title = 'invoice'
    def queryset(self, request, queryset):
        term = self.value()        
        if term is None:
            return
        elif Q(term__icontains='none'):
            any_name = Q(supplier_invoice=None)
            return queryset.filter(any_name).distinct()
        any_name = Q()
        for bit in term.split():
            any_name &= (
                Q(supplier_invoice__supplier_invoice__icontains=bit) |
                Q(supplier_invoice__reference__icontains=bit)
            )        
        return queryset.filter(any_name).distinct()

class PricePOFilter(InputFilter):
    parameter_name = 'po'
    title = 'po'    
    def queryset(self, request, queryset):
        term = self.value()        
        if term is None:
            return        
        any_name = Q()
        for bit in term.split():
            any_name &= (
                Q(supplier_invoice__po__icontains=bit)
            )        
        return queryset.filter(any_name).distinct()