from django.contrib import admin
from django import forms
from .models import *
from django.forms.models import BaseInlineFormSet

class EstimationPartsInline(admin.TabularInline):
    verbose_name_plural = 'parts'
    model = EstimationLine.parts.through
    extra = 1
    autocomplete_fields = ('part',)
    fields = ['part','quantity',]

def AlwaysChangedModelFormParam(request):
    class AlwaysChangedModelForm(forms.ModelForm):
        #def __init__(self,*args,**kwargs):
        #    super(AlwaysChangedModelForm, self).__init__(*args, **kwargs)
        #    print('DEBUG DEBUG DEBUG',request)
        def has_changed(self):
            instance = super(AlwaysChangedModelForm,self).has_changed()
            idcontext = request.GET.get('id')
            if idcontext != None:
                return True 
            """ Should returns True if data differs from initial. 
            By always returning true even unchanged inlines will get validated and saved."""
            return instance
        def save(self,commit=True):
            #print('DEBUGDEBUGDEBUGDEBUGDEBUG')
            instance = super(AlwaysChangedModelForm,self).save(commit=False)
            #print(self)
            if commit:
                instance.save()
            return instance

    return AlwaysChangedModelForm

class WorkOrderPartsInlineFormSet(BaseInlineFormSet):
    model =  WorkOrderLine.parts.through

    def __init__(self, *args, **kwargs):
        super(WorkOrderPartsInlineFormSet, self).__init__(*args, **kwargs)
        idcontext = self.request.GET.get('id')
        #print(idcontext)
        if idcontext != None:
            try:
                estimationline = EstimationLine.objects.get(id=idcontext)
                self.initial = []
                for part in estimationline.parts.all():
                    linepart = LineParts.objects.get(part=part,estimationline=estimationline)
                    self.initial += [{'part':part.pk,'quantity':linepart.quantity}]
            except:
                pass
        #print(self)

def WorkOrderPartsInlineParam(request):
    class WorkOrderPartsInline(admin.TabularInline):
        verbose_name_plural = 'parts'
        model = WorkOrderLine.parts.through
        #extra = 1
        autocomplete_fields = ('part',)
        fields = ['part','quantity',]
        formset = WorkOrderPartsInlineFormSet
        form = AlwaysChangedModelFormParam(request)
        can_delete = True
        def get_formset(self, request, obj=None, **kwargs):
            formset = super(WorkOrderPartsInline, self).get_formset(request, obj, **kwargs)
            formset.request = request
            #print(formset.request)
            return formset

        def get_extra(self, request, obj=None, **kwargs):
            extra = super(WorkOrderPartsInline, self).get_extra(request, obj, **kwargs)
            idcontext = request.GET.get('id')
            #print(idcontext)
            if idcontext != None:
                try:
                    estimationline = EstimationLine.objects.get(id=idcontext)
                    extra = estimationline.parts.all().count()
                except:
                    extra = 1
            else:
                extra = 1
            return extra
    return WorkOrderPartsInline

class InvoicePartsInlineFormSet(BaseInlineFormSet):
    model =  InvoiceLine.parts.through

    def __init__(self, *args, **kwargs):
        super(InvoicePartsInlineFormSet, self).__init__(*args, **kwargs)
        idcontext = self.request.GET.get('id')
        #print(idcontext)
        if idcontext != None:
            try:
                workorderline = WorkOrderLine.objects.get(id=idcontext)
                self.initial = []
                for part in workorderline.parts.all():
                    linepart = LineParts.objects.get(part=part,workorderline=workorderline)
                    self.initial += [{'part':part.pk,'quantity':linepart.quantity}]
            except:
                pass

def InvoicePartsInlineParam(request):
    class InvoicePartsInline(admin.TabularInline):
        verbose_name_plural = 'parts'
        model = InvoiceLine.parts.through
        #extra = 1
        autocomplete_fields = ('part',)
        fields = ['part','quantity',]
        formset = InvoicePartsInlineFormSet
        form = AlwaysChangedModelFormParam(request)
        def get_formset(self, request, obj=None, **kwargs):
            formset = super(InvoicePartsInline, self).get_formset(request, obj, **kwargs)
            formset.request = request
            #print(formset.request)
            return formset

        def get_extra(self, request, obj=None, **kwargs):
            extra = super(InvoicePartsInline, self).get_extra(request, obj, **kwargs)
            idcontext = request.GET.get('id')
            #print(idcontext)
            if idcontext != None:
                try:
                    workorderline = WorkOrderLine.objects.get(id=idcontext)
                    extra = workorderline.parts.all().count()
                except:
                    extra = 1
            else:
                extra = 1
            return extra
    return InvoicePartsInline