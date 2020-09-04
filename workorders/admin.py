from django.contrib import admin
from .models import WorkOrder
from django.db.models import Q
from .inlines import *
from .filters import *
from django.http import HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from django.utils.html import format_html
from django.urls import reverse_lazy
from .forms import *

def export_selected_objects(modeladmin, request, queryset):
    selected = queryset.values_list('pk', flat=True)
    ct = ContentType.objects.get_for_model(queryset.model)
    return HttpResponseRedirect('/workorders/pdf/?ct=%s&ids=%s' % (
        ct.pk,
        '_'.join(str(pk) for pk in selected),
    ))

def make_ongoing(modeladmin, request, queryset):
    from stock.models import InventoryPart
    for line in queryset:
        oldstatus = line.status
        line.status = 'o'
        line.save()
        if oldstatus=='c':
            parts = line.parts.all()
            for part in parts:
                try:
                    invpart = InventoryPart.objects.get(sup_part=part)
                    invpart.save()
                except:
                    pass
make_ongoing.short_description = "Mark as Ongoing"

def make_completed(modeladmin, request, queryset):
    from stock.models import InventoryPart
    for line in queryset:
        oldstatus = line.status
        line.status = 'd'
        line.save()
        if oldstatus=='c':
            parts = line.parts.all()
            for part in parts:
                try:
                    invpart = InventoryPart.objects.get(sup_part=part)
                    invpart.save()
                except:
                    pass
make_completed.short_description = "Mark as Completed"

def make_cancelled(modeladmin, request, queryset):
    from stock.models import InventoryPart
    for line in queryset:
        oldstatus = line.status
        line.status = 'c'
        line.save()
        if oldstatus=='d' or oldstatus=='o':
            parts = line.parts.all()
            for part in parts:
                try:
                    invpart = InventoryPart.objects.get(sup_part=part)
                    invpart.save()
                except:
                    pass
make_cancelled.short_description = "Mark as Cancelled"

def make_billed(modeladmin, request, queryset):
    queryset.update(status='b')
make_billed.short_description = "Mark as Billed"

def make_paid(modeladmin, request, queryset):
    queryset.update(status='p')
make_paid.short_description = "Mark as Paid"

@admin.register(WorkOrderLine)
class WorkOrderLineAdmin(admin.ModelAdmin):
    form = WorkOrderLineAdminForm
    inlines = []
    # such way we send request to main form
    def get_form(self, request, obj=None, **kwargs):
        form = super(WorkOrderLineAdmin, self).get_form(request, obj=obj, **kwargs)
        form.request = request
        return form

    # we define inlines with factory to create Inline class with request inside
    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.inlines = (WorkOrderPartsInlineParam(request), )
        return super(WorkOrderLineAdmin, self).change_view(request, object_id)

    # we define inlines with factory to create Inline class with request inside
    def add_view(self, request, form_url='', extra_context=None):
        self.inlines = (WorkOrderPartsInlineParam(request), )
        return super(WorkOrderLineAdmin, self).add_view(request)
    
    autocomplete_fields = ['order','technician',]
    fields = ['status','order','date','technician','customer_comments','technician_comments','test_results','internal_comments','labour_guide','hours_charged','labour_charged',]
    actions = [make_ongoing,make_cancelled,make_completed,export_selected_objects]
    list_display = ['order','date','contact','vehicle','technician','status','make_invoice']
    #list_display = ['order','status','make_invoice',]
    list_filter = [WorkOrderFilter,TechnicianFilter,ClientFilter,CommentFilter,'status',]
    def get_form(self, request, obj=None, **kwargs):
        form = super(WorkOrderLineAdmin, self).get_form(request, obj=obj, **kwargs)
        form.request = request
        return form
    def contact(self,obj):
        return obj.order.client.clientcontact
    def vehicle(self,obj):
        return obj.order.client.clientvehicle, 'License: %s' % (obj.order.client.licenseplate), 'VIN: %s' % (obj.order.client.vin)
    def make_invoice(self,obj):
        return format_html('<a class="button" href="{}">Convert to Invoice</a>', HttpResponseRedirect('/admin/workorders/invoiceline/add/?id=%s' % (obj.id),).url)
    

@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    search_fields = ('order','client',)
    autocomplete_fields = ('client',)
    #class Media:
    #    js = ('/static/admin/js/hide_attribute.js',)
    '''
    def get_queryset(self, request):
        print('yoooooooooooooo wassup')
        print(self)
        qs = super(PartAdmin, self).get_queryset(request)
        return qs.filter(internal=None)
    '''
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


@admin.register(EstimationLine)
class EstimationLineAdmin(admin.ModelAdmin):
    inlines = [EstimationPartsInline,]
    autocomplete_fields = ['order','technician',]
    fields = ['order','date','technician','customer_comments','technician_comments','test_results','internal_comments','labour_guide','hours_charged','labour_charged',]
    actions = [export_selected_objects]
    #readonly_fields = ('hours_charged',)
    list_display = ['order','date','contact','vehicle','technician','make_wip',]
    list_filter = [EstimationFilter,TechnicianFilter,ClientFilter,CommentFilter,]
    def contact(self,obj):
        return obj.order.client.clientcontact
    def vehicle(self,obj):
        return obj.order.client.clientvehicle, 'License: %s' % (obj.order.client.licenseplate), 'VIN: %s' % (obj.order.client.vin)
    def make_wip(self,obj):
        return format_html('<a class="button" href="{}">Convert to WO</a>', HttpResponseRedirect('/admin/workorders/workorderline/add/?id=%s' % (obj.id),).url)

@admin.register(Estimation)
class EstimationAdmin(admin.ModelAdmin):
    search_fields = ('order','client',)
    autocomplete_fields = ('client',)
    #class Media:
    #    js = ('/static/admin/js/hide_attribute.js',)
    '''
    def get_queryset(self, request):
        print('yoooooooooooooo wassup')
        print(self)
        qs = super(PartAdmin, self).get_queryset(request)
        return qs.filter(internal=None)
    '''
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}

@admin.register(InvoiceLine)
class InvoiceLineAdmin(admin.ModelAdmin):
    form = InvoiceLineAdminForm
    inlines = []
    autocomplete_fields = ['order','technician',]
    fields = ['status','order','date','technician','customer_comments','technician_comments','test_results','internal_comments','labour_guide','hours_charged','labour_charged',]
    actions = [make_billed,make_paid,export_selected_objects]
    list_display = ['order','date','contact','vehicle','technician','status',]
    list_filter = [InvoiceFilter,TechnicianFilter,ClientFilter,CommentFilter,'status',]
    def get_form(self, request, obj=None, **kwargs):
        form = super(InvoiceLineAdmin, self).get_form(request, obj=obj, **kwargs)
        form.request = request
        return form
    def contact(self,obj):
        return obj.order.client.clientcontact
    def vehicle(self,obj):
        return obj.order.client.clientvehicle, 'License: %s' % (obj.order.client.licenseplate), 'VIN: %s' % (obj.order.client.vin)
    def get_form(self, request, obj=None, **kwargs):
        form = super(InvoiceLineAdmin, self).get_form(request, obj=obj, **kwargs)
        form.request = request
        return form

    # we define inlines with factory to create Inline class with request inside
    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.inlines = (InvoicePartsInlineParam(request), )
        return super(InvoiceLineAdmin, self).change_view(request, object_id)

    # we define inlines with factory to create Inline class with request inside
    def add_view(self, request, form_url='', extra_context=None):
        self.inlines = (InvoicePartsInlineParam(request), )
        return super(InvoiceLineAdmin, self).add_view(request)

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    search_fields = ('order','client',)
    autocomplete_fields = ('client',)
    #class Media:
    #    js = ('/static/admin/js/hide_attribute.js',)
    '''
    def get_queryset(self, request):
        print('yoooooooooooooo wassup')
        print(self)
        qs = super(PartAdmin, self).get_queryset(request)
        return qs.filter(internal=None)
    '''
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}
