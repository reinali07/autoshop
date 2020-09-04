from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import Business, Contact, PhoneNumber, Email, SocialMedia
import clientcars_db.models as client_models
'''
class ClientInline(admin.TabularInline):
    verbose_name_plural = "Car Ownership"
    model = client_models.Client.clientcontact.through
    extra = 1
    #autocomplete_fields = ('vehicle__vehicle_makemodel__makemodel')
'''
class BusinessInline(admin.TabularInline):
    verbose_name_plural = "Business Affiliations"
    model = Contact.businesses.through
    extra = 1
    autocomplete_fields = ('business',)

class PhoneInline(GenericTabularInline):
    model = PhoneNumber
    extra = 1

class EmailInline(GenericTabularInline):
    model = Email
    extra = 1

class SocialInline(GenericTabularInline):
    verbose_name_plural = "Social Media"
    model = SocialMedia
    extra = 1
    #autocomplete_fields = ('platform',)