import contacts_db.models as contact_models
import vehicles_db.models as vehicle_models
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey,GenericRelation
from django.utils.html import mark_safe
import uuid


# Create your models here.

def content_file_name(instance, filename):
    #print('uploads/images/contacts/people/{0}-{1}/{2}')
    format = filename.split('.')[-1]
    return 'images/cars/{0}/{1}/{2}/{3}.{4}'.format(instance.clientvehicle.year, instance.clientvehicle.vehicle_makemodel.make,instance.clientvehicle.vehicle_makemodel.vehiclemodel,instance.vin,format)

class Client(models.Model):
    clientcontact = models.ForeignKey(contact_models.Contact,verbose_name="Owner",on_delete=models.CASCADE)
    clientvehicle = models.ForeignKey(vehicle_models.Vehicle,on_delete=models.CASCADE,related_name='client',verbose_name="Vehicle")
    vin = models.CharField('VIN',max_length=17,validators=[RegexValidator('^[0-9a-zA-Z]*$', message="VIN is alphanumeric")])
    licenseplate = models.CharField('License Plate',max_length=15,blank=True)
    comments = models.TextField(max_length=100,blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    colour_choices = [
        ('black', 'Black'),
        ('blue', 'Blue'),
        ('brown', 'Brown'),
        ('red', 'Red'),
        ('silver', 'Silver'),
        ('white', 'White'),
        ('yellow', 'Yellow'),
        ('uk', '--'),
    ]
    colour = models.CharField(max_length=10,choices=colour_choices,default='uk')
    image = models.ImageField(upload_to=content_file_name,blank=True,null=True)

    def save(self,*args,**kwargs):
        accum = list(str(self.vin))
        for i in range(0,len(accum),1):
            accum[i] = '1' if accum[i] == 'I' else accum[i]
            accum[i] = '0' if accum[i] == 'O' else accum[i]
        self.vin = (''.join(accum)).upper()
        return super(Client, self).save(*args, **kwargs)
    def __str__(self):
        return "%s %s %s %s" % (str(self.clientcontact.__str__()),str(self.clientvehicle.__str__()),str(self.licenseplate),str(self.vin))
