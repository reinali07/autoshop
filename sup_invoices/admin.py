from django.contrib import admin
from .models import *
from .inlines import *
from .forms import *
from django.utils.html import format_html
from .filters import *
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from .forms import *

# Register your models here.

def export_selected_objects(modeladmin, request, queryset):
    selected = queryset.values_list('pk', flat=True)
    return HttpResponseRedirect('/sup_invoices/pdf/?ids=%s' % (
        '_'.join(str(pk) for pk in selected),
    ))

#@admin.register(SupplierInvoice)
#class SupplierInvoiceAdmin(CloneModelAdmin):
@admin.register(SupplierInvoice)
class SupplierInvoiceAdmin(admin.ModelAdmin):
    change_form_template='admin/sup_invoices/supplierinvoice/change_form.html'
    form = SupplierInvoiceAdminForm
    inlines = []
    actions = [export_selected_objects,]
    # send request to main form
    def get_form(self, request, obj=None, **kwargs):
        form = super(SupplierInvoiceAdmin, self).get_form(request, obj=obj, **kwargs)
        form.request = request
        return form
    # we define inlines with factory to create Inline class with request inside
    def change_view(self, request, object_id, form_url='', extra_context=None):
        if SupplierInvoice.objects.get(id=object_id).is_return:
            request.GET = request.GET.copy()
            request.GET['return'] = True
        self.inlines = (SupplierInvoicePartsInlineParam(request), )
        return super(SupplierInvoiceAdmin, self).change_view(request, object_id)

    # we define inlines with factory to create Inline class with request inside
    def add_view(self, request, form_url='', extra_context=None):
        self.inlines = (SupplierInvoicePartsInlineParam(request), )
        return super(SupplierInvoiceAdmin, self).add_view(request)
    
    autocomplete_fields = ('supplier',)
    #include_duplicate_action = False
    #include_duplicate_object_link = False
    #exclude = ['reference',]

    def delete_supplier_invoice(self, obj):
        return format_html('<a class="button" href="/admin/sup_invoices/supplierinvoice/{}/delete/">Delete</a>', obj.id)
    #def returnedqty_disp(self,obj):
    #    return SupplierInvoiceParts.objects.get(supplier_invoice=obj,part=435345).returnedqty
        #return obj.purchased_parts.all()[:1].get().returnedqty
        #return True
    #def retqty_disp(self,obj):
    #    return SupplierInvoiceParts.objects.get(supplier_invoice=obj,part=435345).retqty
    def make_return(self,obj):
        if not obj.is_return:
            #return format_html('<a class="button" href="/sup_invoices/supplier_invoice/{}/make_return">Return</a>',obj.id)
            return format_html('<a class="button" href="{}">Make Return</a>', HttpResponseRedirect('/admin/sup_invoices/supplierinvoice/add/?id=%s' % (obj.id),).url)
        else:
            return format_html('Return')

    list_display = ['supplier_invoice','reference','po','is_return','make_return','delete_supplier_invoice',]
    #readonly_fields = ['is_return',]
    list_filter = [ReferenceFilter,POFilter,PartFilter,'is_return',]
    '''
    def get_form(self, request, obj=None, **kwargs):
        #print('hehe')
        if obj and obj.is_return:
            self.exclude = []
            #self.readonly_fields = ['reference','is_return','supplier','po',]
        else:
            #self.readonly_fields = ['is_return',]
            self.fields = ['supplier_invoice','po','date','supplier','is_return',]
        #return form
        return super(SupplierInvoiceAdmin, self).get_form(request, obj, **kwargs)
    '''
    #class Media:
    #    js = ('/static/admin/js/hide_attribute.js',)

@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    from stock.inlines import PartInline
    search_fields = ('part','description','internal__part_number',)
    exclude = ('part','quantity','internal',)
    #class Media:
    #    js = ('/static/admin/js/hide_attribute.js',)
    '''
    def get_queryset(self, request):
        print('yoooooooooooooo wassup')
        print(self)
        qs = super(PartAdmin, self).get_queryset(request)
        return qs.filter(internal=None)
    '''
    
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        #print(queryset.filter(internal=None))
        #print(request.GET['field_name'])
        #print(request.GET)
        #print(request.GET.get['page'])
        try:
            if 'InventoryPart_sup_part' in request.GET['field_name']:
                queryset = queryset.filter(internal=None)
        except:
            pass
        return queryset, use_distinct
    
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}

@admin.register(SupplierInvoiceParts)
class SupplierInvoicePartsAdmin(admin.ModelAdmin):
    change_list_template = 'admin/sup_invoices/supplierinvoiceparts/change_list.html'
    search_fields = ('part',)
    def price(self):
        return '$' + str(self.list_price)
    def part_number(self):
        return str(self.part)
    def invoice_number(self):
        try:
            return str(self.supplier_invoice)
        except:
            return None
    def internal_part_number(self):
        return str(self.part.internal.all()[:1].get().part_number)
    def po(self):
        try:
            return str(self.supplier_invoice.po)
        except:
            return None
    def supplier(self):
        try:
            return str(self.supplier_invoice.supplier)
        except:
            return str(self.supplier)
    def date(self):
        try:
            return str(self.supplier_invoice.date)
        except:
            return str(self.date)
    list_display = (internal_part_number,supplier,part_number,price,date,invoice_number,po,)
    ordering = ('list_price',)
    list_filter = [PricePartFilter,InvoiceFilter,PricePOFilter,]
    exclude = ('prices','supplier_invoice','quantity','returnedqty','retqty','core',)
    fieldsets = [
        (None, {
            'fields': [('supplier','part','date',),('list_price','cost','is_promo','package_size',),]
        }),
    ]
    def get_form(self, request, obj=None, **kwargs):
        #print('hehe')
        if obj and obj.supplier_invoice:
            self.readonly_fields = ['supplier','part','date','list_price','cost','is_promo','package_size',]
        else:
            self.readonly_fields = []
        return super(SupplierInvoicePartsAdmin, self).get_form(request, obj, **kwargs)

    def get_queryset(self, request):
        qs = super(SupplierInvoicePartsAdmin, self).get_queryset(request)
        return qs.filter(Q(supplier_invoice__is_return=False)|Q(supplier_invoice=None))
    def has_add_permission(self, request): 
        return False

#admin.site.register(PO,POAdmin)
#admin.site.register(Part,PartAdmin)


@admin.register(Prices)
class PricesAdmin(admin.ModelAdmin):
    change_form_template='admin/sup_invoices/supplierinvoiceparts/change_form.html'
    inlines = [BulkAddInline,]
    def response_add(self, request, obj, post_url_continue="../%s/"):
        if '_continue' not in request.POST:
            return HttpResponseRedirect(reverse("admin:sup_invoices_supplierinvoiceparts_changelist"))
        else:
            return super(PricesAdmin, self).response_add(request, obj, post_url_continue)

    def response_change(self, request, obj):
        if '_continue' not in request.POST:
            return HttpResponseRedirect(reverse("admin:sup_invoices_supplierinvoiceparts_changelist"))
        else:
            return super(PricesAdmin, self).response_change(request, obj)

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}
