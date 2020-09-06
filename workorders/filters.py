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

class WorkOrderFilter(InputFilter):
    parameter_name = 'workorder_number'
    title = 'workorder number'    
    def queryset(self, request, queryset):
        term = self.value()        
        if term is None:
            return        
        any_name = Q()
        for bit in term.split():
            any_name &= (
                Q(order__workorder__icontains=bit)
            )        
        return queryset.filter(any_name).distinct()

class EstimationFilter(InputFilter):
    parameter_name = 'estimation_number'
    title = 'estimation number'    
    def queryset(self, request, queryset):
        term = self.value()        
        if term is None:
            return        
        any_name = Q()
        for bit in term.split():
            any_name &= (
                Q(order__estimation__icontains=bit)
            )        
        return queryset.filter(any_name).distinct()

class InvoiceFilter(InputFilter):
    parameter_name = 'invoice_number'
    title = 'invoice number'    
    def queryset(self, request, queryset):
        term = self.value()        
        if term is None:
            return        
        any_name = Q()
        for bit in term.split():
            any_name &= (
                Q(order__invoice__icontains=bit)
            )        
        return queryset.filter(any_name).distinct()

class TechnicianFilter(InputFilter):
    parameter_name = 'technician'
    title = 'technician'    
    def queryset(self, request, queryset):
        term = self.value()        
        if term is None:
            return        
        any_name = Q()
        for bit in term.split():
            any_name &= (
                Q(technician__first_name__icontains=bit) |
                Q(technician__last_name__icontains=bit)  |
                Q(technician__nickname__icontains=bit)
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
                Q(customer_comments__icontains=bit) |
                Q(technician_comments__icontains=bit) |
                Q(test_results__icontains=bit) |
                Q(internal_comments__icontains=bit)
            )        
        return queryset.filter(any_name).distinct()

class ClientFilter(InputFilter):
    parameter_name = 'client'
    title = 'client'    
    def queryset(self, request, queryset):
        term = self.value()        
        if term is None:
            return        
        any_name = Q()
        for bit in term.split():
            any_name &= (
                Q(order__client__vin__icontains=bit) |
                Q(order__client__clientcontact__first_name__icontains=bit) |
                Q(order__client__clientcontact__last_name__icontains=bit) |
                Q(order__client__clientcontact__nickname__icontains=bit) |
                Q(order__client__clientvehicle__vehicle_makemodel__makemodel__icontains=bit) |
                Q(order__client__clientvehicle__year__icontains=bit) |
                Q(order__client__licenseplate__icontains=bit)
            )        
        return queryset.filter(any_name).distinct()