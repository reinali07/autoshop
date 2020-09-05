from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse,reverse_lazy
from django.views import generic
from .models import *
from sup_invoices.models import Part
from django.template.loader import get_template
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from preferences import preferences

from .utils import render_to_pdf

class GeneratePdf(generic.View):
    def get(self, request, *args, **kwargs):
        template = get_template('workorders/workorder_pdf.html')
        idcontext = self.request.GET.get('ids')
        ids = idcontext.split('_')
        content = ContentType.objects.get(pk=self.request.GET.get('ct'))
        model = content.model_class()
        qs = model.objects.none()
        #print(self.request)
        for id in ids:
            qs = qs | model.objects.filter(pk=id)
        qs = qs.order_by('order')
        #print(qs)
        doctype = type(qs.first().order).__name__
        sorted_jobs = [model.objects.filter(pk=qs.first().pk)]
        numbers = str(qs.first().order)
        qs = qs.exclude(pk=qs.first().pk)
        for job in qs:
            if job.order == sorted_jobs[-1].all().first().order:
                #print(qs.get(pk=job.pk).order.client.clientcontact.all()[0].first_name)
                sorted_jobs[-1] |= qs.filter(pk=job.pk)
                #print('ha')
            else:
                sorted_jobs += [qs.filter(pk=job.pk)]
                numbers += '_' + str(qs.get(pk=job.pk).order)
        context = {
             'sorted_jobs': sorted_jobs,
             'model':doctype,
        }
        html = template.render(context)
        pdf = render_to_pdf('workorders/workorder_pdf.html', context)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="%s-%s.pdf"' % (doctype,numbers)
        return response

def get_defaults(request):
    data = {'hours':float(request.GET.get('value')) * preferences.GlobalPreference.labour_markup,'labour':float(request.GET.get('value')) * preferences.GlobalPreference.labour_markup * preferences.GlobalPreference.labour_rate}
    return JsonResponse(data)