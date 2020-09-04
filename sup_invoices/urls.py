from django.urls import path,include
from . import views

app_name = 'sup_invoices'
urlpatterns = [
    path('pdf/',views.GeneratePdf.as_view(),name='pdf'),
    path('get_units/',views.get_unit,name='get_unit'),
]