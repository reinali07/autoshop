from django.db import models
from phone_field import PhoneField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey,GenericRelation
from s3direct.fields import S3DirectField


#from clientcars_db import models as client_models
#import clientcars_db.models as client_models


# Create your models here.

class PhoneNumber(models.Model):
    home = 'home phone'
    cell = 'cell phone'
    work = 'work phone'
    fax = 'fax'
    other = 'other'
    phone_type_choices = [
        (home, 'Home Phone'),
        (cell, 'Cell Phone'),
        (work, 'Work Phone'),
        (fax, 'Fax'),
        (other, 'Other'),
    ]
    phone_type = models.CharField(max_length=20,choices=phone_type_choices,default=cell)
    phonenumber = PhoneField(blank=True, help_text='Contact phone number',unique = True)

    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return str(self.phonenumber)
    
class Email(models.Model):
    email = models.EmailField(max_length=200,unique = True)

    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return str(self.email)

class SocialMedia(models.Model):
    platform = models.CharField(max_length=100)
    socialmedia = models.CharField('Social Media',max_length=100)

    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return str(self.socialmedia)

def business_content_file_name(instance, filename):
    #print('uploads/images/contacts/people/{0}-{1}/{2}')
    format = filename.split('.')[-1]
    return 'images/contacts/businesses/{0}.{1}'.format(instance.business,format)

class Business(models.Model):
    business = models.CharField(max_length=200)
    business_type = models.CharField(max_length=200,blank=True)

    #cars = GenericRelation(client_models.Client,related_query_name='businesses')
    phones = GenericRelation(PhoneNumber,related_query_name='phones')
    emails = GenericRelation(Email,related_query_name='emails')
    socials = GenericRelation(SocialMedia,related_query_name='socials')
    
    discount_rate = models.FloatField(null=True,blank=True)
    comments = models.TextField(max_length=200,blank=True)
    image = models.ImageField(upload_to=business_content_file_name,blank=True,null=True)

    class Meta:
        verbose_name_plural = "businesses"
    def __str__(self):
        return str(self.business)

def content_file_name(instance, filename):
    #print('uploads/images/contacts/people/{0}-{1}/{2}')
    format = filename.split('.')[-1]
    return 'images/contacts/people/{0}-{1}.{2}'.format(instance.first_name, instance.last_name,format)

class Contact(models.Model):
    #cars = GenericRelation(client_models.Client,related_query_name='contacts')
    phones = GenericRelation(PhoneNumber,related_query_name='phones')
    emails = GenericRelation(Email,related_query_name='emails')
    socials = GenericRelation(SocialMedia,related_query_name='socials')

    businesses = models.ManyToManyField(Business,related_name='contacts',default='')
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    nickname = models.CharField(max_length=200,blank=True)
    discount_rate = models.FloatField(null=True,blank=True)
    comments = models.TextField(max_length=200,blank=True)
    image = models.ImageField(upload_to=content_file_name,blank=True,null=True)
    is_tech = models.BooleanField('Technician?',default=False)
    images3 = S3DirectField(dest='primary_destination', blank=True)

    def __str__(self):
        return str(self.first_name) + ' ' + str(self.last_name)
    