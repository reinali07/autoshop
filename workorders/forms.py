from .models import *
from django import forms

class WorkOrderLineAdminForm(forms.ModelForm):
    class Meta:
        model = WorkOrderLine
        fields = ('__all__')
    def __init__(self, *args, **kwargs):
        super(WorkOrderLineAdminForm, self).__init__(*args, **kwargs)
        #print(kwargs)
        idcontext = self.request.GET.get('id')
        #print(idcontext)
        #self.fields['hours_charged'].disabled = True
        if idcontext != None:
            try:
                estimationline = EstimationLine.objects.get(id=idcontext)
                self.fields['technician'].initial = estimationline.technician
                #print('hey')
                self.fields['customer_comments'].initial = estimationline.customer_comments
                #print('hey')
                self.fields['technician_comments'].initial = estimationline.technician_comments
                #print('hey')
                self.fields['test_results'].initial = estimationline.test_results
                #print('hey')
                self.fields['internal_comments'].initial = estimationline.internal_comments
                #print('hey')
                self.fields['hours_charged'].initial = estimationline.hours_charged
                #print('hey')
                self.fields['labour_charged'].initial = estimationline.labour_charged
                #print('hey')
                self.fields['labour_guide'].initial = estimationline.labour_guide
                #print(self.fields['labour_charged'].initial)
            except:
                pass
        self.fields['hours_charged'].widget = forms.HiddenInput()
        self.fields['labour_charged'].widget = forms.HiddenInput()
        widget = self.fields['technician'].widget
        widget.can_delete_related = False

class InvoiceLineAdminForm(forms.ModelForm):
    class Meta:
        model = InvoiceLine
        fields = ('__all__')
    def __init__(self, *args, **kwargs):
        super(InvoiceLineAdminForm, self).__init__(*args, **kwargs)
        #print(kwargs)
        #self.fields['hours_charged'].disabled = True
        idcontext = self.request.GET.get('id')
        #print(idcontext)
        if idcontext != None:
            try:
                workorderline = WorkOrderLine.objects.get(id=idcontext)
                self.fields['technician'].initial = workorderline.technician
                self.fields['customer_comments'].initial = workorderline.customer_comments
                self.fields['technician_comments'].initial = workorderline.technician_comments
                self.fields['test_results'].initial = workorderline.test_results
                self.fields['internal_comments'].initial = workorderline.internal_comments
                self.fields['hours_charged'].initial = workorderline.hours_charged
                self.fields['labour_charged'].initial = workorderline.labour_charged
                self.fields['labour_guide'].initial = workorderline.labour_guide
            except:
                pass