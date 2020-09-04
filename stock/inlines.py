from django.contrib import admin
from .models import *
from sup_invoices.models import Part
from django.db.models import Q
from django.urls import resolve
from django.forms.models import BaseInlineFormSet
from django.utils.html import format_html
from .forms import *


'''
class LimitModelFormset(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(LimitModelFormset, self).__init__(*args, **kwargs)
        self.fields['part'].queryset = Part.objects.filter(internal=None)
'''
class PartInline(admin.TabularInline):
    template = 'admin/inventorypart/edit_inline/tabular.html'
    model = InventoryPart.sup_part.through
    extra = 1
    autocomplete_fields = ('part',)
    #readonly_fields = ('stock',)
    search_field = ('part',)
    #def stock(self,obj):
    #    return format_html('<span class="quantity_tag"></span>')
'''
class PartInline(admin.TabularInline):
    #formset = LimitModelFormset
    model = InventoryPart.sup_part.through
    extra = 1
    autocomplete_fields = ('part',)
    readonly_fields = ('quantity',)
    def quantity(self,obj):
        return format_html('<span class="quantity_tag"></span>')
'''
'''
    def get_queryset(self, request):
        resolved = resolve(request.path_info)
        parent = self.parent_model.objects.get(pk=resolved.kwargs['object_id'])
        print('yoooooooooooooo wassup')
        qs = super(PartInline, self).get_queryset(request)
        #print(qs[:1].get().part.internal.all())
        available = qs.filter(inventorypart=None)
        current = qs.filter(inventorypart=parent)
        print(current)
        return qs.filter(Q(inventorypart=parent)|Q(inventorypart=None))
    '''
#class PartInline(admin.TabularInline):
#    model = Part
    