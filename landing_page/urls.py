from django.urls import path,include
from . import views

app_name = 'stock'
urlpatterns = [
    path('',views.redirect,name='index'),
    path('test/', views.test, name='test'),
]