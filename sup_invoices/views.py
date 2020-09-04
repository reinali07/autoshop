from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse,reverse_lazy
from django.views import generic
from .models import *
from django.template.loader import get_template
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse


from .utils import render_to_pdf

class GeneratePdf(generic.View):
    def get(self, request, *args, **kwargs):
        template = get_template('sup_invoices/invoice_pdf.html')
        idcontext = self.request.GET.get('ids')
        ids = idcontext.split('_')
        qs = SupplierInvoice.objects.none()
        #print(self.request)
        for id in ids:
            qs = qs | SupplierInvoice.objects.filter(pk=id)
        qs = qs.order_by('po')
        #print(qs)
        sorted_invoices = [SupplierInvoice.objects.filter(pk=qs.first().pk)]
        numbers = str(qs.first().po)
        qs = qs.exclude(pk=qs.first().pk)
        for invoice in qs:
            if invoice.po == sorted_invoices[-1].all().first().po:
                #print(qs.get(pk=job.pk).order.client.clientcontact.all()[0].first_name)
                sorted_invoices[-1] |= qs.filter(pk=invoice.pk)
                #print('h')
            else:
                sorted_invoices += [qs.filter(pk=invoice.pk)]
                numbers += '_' + str(qs.get(pk=invoice.pk).po)
        context = {
             'sorted_invoices': sorted_invoices,
        }
        html = template.render(context)
        #response = template.render(context)
        pdf = render_to_pdf('sup_invoices/invoice_pdf.html', context)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="Invoice-%s.pdf"' % (numbers)
        return response


def get_unit(request):
    #print(request.GET)
    #print(self.data)
    idcontext = request.GET.get('id')
    #print(idcontext)
    part_data = idcontext.split(':')
    part_data[1] = part_data[1].replace(" ","")
    #print(part_data)
    #print(Part.objects.get(pk=idcontext).internal.all().first().standard_unit)
    try:
        unit = str(Part.objects.get(brand=part_data[0],part_number=part_data[1]).internal.all().first().standard_unit)
    except:
        unit = ''
    data = {'unit':unit}
    #print(data)
    #print(data)
    return JsonResponse(data)