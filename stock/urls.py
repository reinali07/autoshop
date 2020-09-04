from django.urls import path,include
from . import views

app_name = 'stock'
urlpatterns = [
    path('get_quantity/',views.get_quantity,name='get_quantity'),
]