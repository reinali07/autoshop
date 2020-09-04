from django.contrib import admin
from .models import *
from .inlines import *
from .filters import *
from sup_invoices.models import Part

# Register your models here.
@admin.register(InventoryPart)
class InventoryPartAdmin(admin.ModelAdmin):
    #formset = LimitModelFormset
    change_form_template='admin/inventorypart/change_form.html'
    inlines = [PartInline,]
    #filter_horizontal = ('sup_part',)
    #exclude = ('sup_part',)
    fieldsets = [
        (None, {
            'fields': ['part_number','stock',('min_stock','full_stock'),('area','row','line'),'average_price','description','standard_unit',]
        }),
        #('Parts', {
        #    'fields': ['sup_part',]
        #})
    ]
    #filter_horizontal = ['sup_part',]
    list_display = ['__str__','stock','min_stock','area','row','line','needs_restock']
    list_filter = [PartNumberFilter,PartFilter,NeedsRestockFilter,]
    #def save_model(self, request, obj, form, change):
    #    obj.save()
    #    obj.update_sup_part()
    #def formfield_for_manytomany(self, db_field, request, **kwargs):
    #    if db_field.name == "sup_part":
    #        kwargs["queryset"] = Part.objects.filter(internal=None)
    #    return super(InventoryPartAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

#admin.site.register(InventoryPart)
