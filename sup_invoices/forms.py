from django import forms
from .models import SupplierInvoice

class ReturnActionForm(forms.Form):
    return_order = forms.BooleanField(required=False,)
    def form_action(self):
        if self.cleaned_data.get('return_order', False):
            self.make_clone(attrs={'is_return': True})
        return super(SupplierInvoice, self).save(*args, **kwargs)
    def save(self, account, user):
        if self.cleaned_data.get('return_order', False):
            self.make_clone(attrs={'is_return': True})
        return super(SupplierInvoice, self).save(*args, **kwargs)

class SupplierInvoiceAdminForm(forms.ModelForm):
    class Meta:
        model = SupplierInvoice
        fields = ('__all__')
    def __init__(self, *args, **kwargs):
        super(SupplierInvoiceAdminForm, self).__init__(*args, **kwargs)
        #print(kwargs)
        idcontext = self.request.GET.get('id')
            #print(idcontext)
        try:
            is_return = kwargs['instance'].is_return
        except:
            is_return = False
        if idcontext != None or is_return:
            try:
                supplierinvoice = SupplierInvoice.objects.get(id=idcontext)
                #print(supplierinvoice)
                #self.fields['supplier_invoice'].initial = supplierinvoice.supplier_invoice
                self.fields['po'].initial = supplierinvoice.po
                #print('c')
                self.fields['is_return'].initial = True
                #print('a')
                #print(supplierinvoice.reference)
                self.fields['reference'].initial = supplierinvoice.reference
                #print('y')
                self.fields['supplier'].initial = supplierinvoice.supplier
                self.fields['comments'].initial = supplierinvoice.comments
                #print('h')
                #print(self.fields)
                self.data._mutable = True
                self.data.update({ 'po': supplierinvoice.po,'is_return': True,'supplier': supplierinvoice.supplier,'reference':supplierinvoice.reference })
                self.data._mutable = False
            except:
                pass
            self.fields['po'].disabled = True
            self.fields['supplier'].disabled = True
            #self.fields['po'].widget.attrs['disabled'] = True
            #self.fields['supplier'].widget.attrs['disabled'] = True
            widget = self.fields['supplier'].widget
            widget.can_add_related = False
            widget.can_change_related = False
            widget.can_delete_related = False
        self.fields['reference'].widget = forms.HiddenInput()
        self.fields['is_return'].disabled = True
        #print(self.data)
        #self.fields['reference'].disabled = True
    def has_changed(self):
        instance = super(SupplierInvoiceAdminForm,self).has_changed()
        idcontext = request.GET.get('id')
        if idcontext != None:
            return True 
        """ Should returns True if data differs from initial. 
        By always returning true even unchanged inlines will get validated and saved."""
        return instance

def SupplierPartsInvoiceFormParam(request):
    class SupplierPartsInvoiceInlineForm(forms.ModelForm):
        class Meta:
            model = SupplierInvoice.purchased_parts.through
            fields = ('__all__')
        def __init__(self, *args, **kwargs):
            super(SupplierPartsInvoiceInlineForm, self).__init__(*args, **kwargs)
            #print(request.GET)
            idcontext = request.GET.get('id')
            is_return = request.GET.get('return')
            #print(idcontext)
            #print(kwargs)
            if idcontext != None or is_return:
                #print('yippy')
                #self.fields['part'].widget.attrs['disabled'] = True
                #self.fields['cost'].widget.attrs['disabled'] = True
                #self.fields['quantity'].widget.attrs['disabled'] = True
                #self.fields['list_price'].widget.attrs['disabled'] = True
                #self.fields['is_promo'].widget.attrs['disabled'] = True
                #self.fields['package_size'].widget.attrs['disabled'] = True
                self.fields['part'].disabled = True
                self.fields['cost'].disabled = True
                self.fields['quantity'].disabled = True
                self.fields['returnedqty'].disabled = True
                self.fields['list_price'].disabled = True
                self.fields['is_promo'].disabled = True
                self.fields['package_size'].disabled = True
                widget = self.fields['part'].widget
                widget.can_add_related = False
                widget.can_change_related = False
                widget.can_delete_related = False
        def has_changed(self):
            instance = super(SupplierPartsInvoiceInlineForm,self).has_changed()
            idcontext = request.GET.get('id')
            if idcontext != None:
                return True 
            """ Should returns True if data differs from initial. 
            By always returning true even unchanged inlines will get validated and saved."""
            return instance
        def has_add_permission(self, request):
            return False

    return SupplierPartsInvoiceInlineForm