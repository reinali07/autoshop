from django.db.models import Q
from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.db.models import F

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

class PartNumberFilter(InputFilter):
    parameter_name = 'internal_part'
    title = 'internal part number'    
    def queryset(self, request, queryset):
        term = self.value()        
        if term is None:
            return        
        any_name = Q()
        for bit in term.split():
            any_name &= (
                Q(part_number__icontains=bit)
            )        
        return queryset.filter(any_name).distinct()

class PartFilter(InputFilter):
    parameter_name = 'part'
    title = 'parts'    
    def queryset(self, request, queryset):
        term = self.value()        
        if term is None:
            return        
        any_name = Q()
        for bit in term.split():
            any_name &= (
                Q(sup_part__part__icontains=bit)
            )
        return queryset.filter(any_name).distinct()

class NeedsRestockFilter(admin.SimpleListFilter):
    title = 'stock'
    parameter_name = 'needs_restock'

    def lookups(self, request, model_admin):
        return (
            ('Needs Restock', 'Needs Restock'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Needs Restock':
            return queryset.exclude(stock__gte=F('min_stock'))
        return queryset