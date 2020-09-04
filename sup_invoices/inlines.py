from django.contrib import admin
from django import forms
from .models import *
from django.forms.models import BaseInlineFormSet
from contacts_db.models import Business
from .forms import *
from django.utils.html import format_html
from django.contrib.admin.widgets import AutocompleteSelect


class AlwaysChangedModelForm(forms.ModelForm):
    def has_changed(self):
        """ Should returns True if data differs from initial. 
        By always returning true even unchanged inlines will get validated and saved."""
        return True

class SupplierInvoicePartsInlineFormSet(BaseInlineFormSet):
    model = SupplierInvoice.purchased_parts.through

    def __init__(self, *args, **kwargs):
        super(SupplierInvoicePartsInlineFormSet, self).__init__(*args, **kwargs)
        idcontext = self.request.GET.get('id')
        #print(idcontext)
        if idcontext != None:
            try:
                supplierinvoice = SupplierInvoice.objects.get(id=idcontext)
                self.initial = []
                for part in supplierinvoice.purchased_parts.all():
                    supplierinvoiceparts = SupplierInvoiceParts.objects.get(supplier_invoice=supplierinvoice,part=part)
                    self.initial += [{'part':part.pk,'quantity':supplierinvoiceparts.quantity,'returnedqty':supplierinvoiceparts.returnedqty,'list_price':supplierinvoiceparts.list_price,'cost':supplierinvoiceparts.cost,'is_promo':supplierinvoiceparts.is_promo,'package_size':supplierinvoiceparts.package_size,}]
            except:
                pass

def SupplierInvoicePartsInlineParam(request):
    class SupplierInvoicePartsInline(admin.TabularInline):
        template = 'admin/sup_invoices/supplierinvoice/edit_inline/tabular.html'
        verbose_name_plural = 'parts'
        #model = SupplierInvoiceParts
        model = SupplierInvoice.purchased_parts.through
        fields = ('part','quantity','returnedqty','list_price','cost','is_promo','package_size',)
        exclude = ['retqty']
        readonly_fields = ['returnedqty',]
        #extra = 0
        autocomplete_fields = ('part',)
        formset = SupplierInvoicePartsInlineFormSet
        form = SupplierPartsInvoiceFormParam(request)
        #def unit(self,obj):
        #    #return format_html('lol')
        #    return format_html('<span class="unit_tag"></span>')
        formfield_overrides = {
            models.FloatField: {'widget': forms.NumberInput(attrs={'size':10})},
            models.PositiveIntegerField: {'widget': forms.NumberInput(attrs={'size':10})},
            models.DecimalField: {'widget': forms.NumberInput(attrs={'size':10})},
        }
        def get_formset(self, request, obj=None, **kwargs):
            #print('hehe')
            #print(request)
            idcontext = request.GET.get('id')
            #print(obj)
            if obj and obj.is_return:
                #print('ye')
                self.fields = ('part','quantity','returnedqty','retqty','list_price','cost','is_promo','package_size',)
                self.exclude = []
                #self.readonly_fields = ['part','returnedqty','quantity','list_price','cost','is_promo','package_size',]
                self.readonly_fields = []
                #self.extra = 0
                self.max_num = obj.purchased_parts.all().count()
                self.min_num = self.max_num
                self.can_delete = False
                #widget = form.base_fields['part'].widget
                #widget.can_add_related = False
                #widget.can_change_related = False
            elif obj and not obj.is_return:
                self.fields = ('part','quantity','returnedqty','list_price','cost','is_promo','package_size',)
                self.exclude = ['retqty']
                self.readonly_fields = ['returnedqty',]
                #self.extra = 0
            elif idcontext != None:
                self.fields = ('part','quantity','returnedqty','retqty','list_price','cost','is_promo','package_size',)
                self.readonly_fields = []
                self.exclude = []
                #self.extra = 0
                self.can_delete = False
                #widget = form.base_fields['part'].widget
                #widget.can_add_related = False
                #widget.can_change_related = False
                try:
                    supplierinvoice = SupplierInvoice.objects.get(id=idcontext)
                    self.max_num = supplierinvoice.purchased_parts.all().count()
                    self.min_num = self.max_num
                except:
                    pass
            formset = super(SupplierInvoicePartsInline, self).get_formset(request, obj, **kwargs)
            formset.request = request
            form = formset.form
            return formset
            #return super(SupplierInvoicePartsInline, self).get_formset(request, obj, **kwargs)
        def get_extra(self, request, obj=None, **kwargs):
            extra = super(SupplierInvoicePartsInline, self).get_extra(request, obj, **kwargs)
            idcontext = request.GET.get('id')
            #print(idcontext)
            extra = 0
            if idcontext == None and not obj:
                extra = 1
                #try:
                #    supplierinvoice = SupplierInvoice.objects.get(id=idcontext)
                #    extra = supplierinvoice.purchased_parts.all().count()
                #except:
                #    extra = 0
            #else:
            #    extra = 0
            return extra
    return SupplierInvoicePartsInline

class SupplierInline(admin.TabularInline):
    verbose_name = 'supplier'
    model = Business
    extra = 1
    autocomplete_fields = ('business',)


class BulkAddForm(forms.ModelForm):
    class Meta:
        widgets = {
            'supplier': AutocompleteSelect(
                SupplierInvoiceParts._meta.get_field('supplier').remote_field,
                admin.site,
                attrs={'data-dropdown-auto-width': 'true','style':'width:100px'}
            ),
            'part': AutocompleteSelect(
                SupplierInvoiceParts._meta.get_field('part').remote_field,
                admin.site,
                attrs={'data-dropdown-auto-width': 'true','style':'width:100px'}
            ),
        }

class BulkAddInline(admin.TabularInline):
    verbose_name_plural = 'parts'
    #model = Prices.history.through
    model = SupplierInvoiceParts
    fields = ('supplier','part','list_price','is_promo','date','package_size','unit','comments',)
    readonly_fields = ('unit',)
    #exclude = ['retqty','returnedqty',]
    extra = 1
    #autocomplete_fields = ('part','supplier')
    form = BulkAddForm
    formfield_overrides = {
        models.FloatField: {'widget': forms.NumberInput(attrs={'size':7})},
        models.PositiveIntegerField: {'widget': forms.NumberInput(attrs={'size':7})},
        models.DecimalField: {'widget': forms.NumberInput(attrs={'size':7})},
        models.TextField: {'widget': forms.TextInput(attrs={'size':30})},
    }
    def unit(self,obj):
        return format_html('<span class="unit_tag"></span>')