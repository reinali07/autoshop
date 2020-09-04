from django.shortcuts import render
from sup_invoices.models import Part
from django.http import JsonResponse

'''
from dal import autocomplete

class PartAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Part.objects.all()
    
        if self.q:
            qs = qs.filter(internal=None)
    
        return qs
# Create your views here.
'''

def get_quantity(request):
    #print(request.GET)
    #print(self.data)
    idcontext = request.GET.get('id')
    part_data = idcontext.split(':')
    part_data[1] = part_data[1].replace(" ","")
    #print(part_data)
    #print(Part.objects.get(pk=idcontext).internal.all().first().standard_unit)
    try:
        quantity = str(Part.objects.get(brand=part_data[0],part_number=part_data[1]).quantity)
    except:
        quantity = 'yes'
    data = {'quantity':quantity}
    return JsonResponse(data)