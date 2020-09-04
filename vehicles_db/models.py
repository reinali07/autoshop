from django.db import models
from django.db import IntegrityError
import datetime
import uuid
from django.core.validators import RegexValidator


'''
class Year(models.Model):
    YEAR_CHOICES = []
    for r in range(1980, (datetime.datetime.now().year+5)):
        YEAR_CHOICES.append((r,r))
    year = models.IntegerField(choices=YEAR_CHOICES,unique=True,default=datetime.datetime.now().year)
    def __str__(self):
        return str(self.year)
'''
'''
class Make(models.Model):
    make = models.CharField(max_length=100)
    strid = models.CharField(max_length=100)
    def save(self, *args, **kwargs):
        repeated = False
        self.strid = self.make.lower()
        for i in Make.objects.all():
            if str(self.strid) == str(i.strid):
                self.make = i.make
                repeated = True
                break
            
        if repeated == False:
            return super(Make, self).save(*args, **kwargs)
    def __str__(self):
        return str(self.make) + ' ' + str(self.vehicle_model)

'''

class MakeModel(models.Model):
    make = models.CharField('Make',max_length=100)
    vehiclemodel = models.CharField('Model',max_length=100)
    #stridmake = models.CharField(max_length=100,blank=True)
    #stridmodel = models.CharField(max_length=100,blank=True)
    makemodel = models.CharField('Make and Model',max_length=100)
    comments = models.CharField(max_length=50,blank=True)
    #class Meta:
    #    unique_together = ('make', 'vehiclemodel',)
    def save(self, *args, **kwargs):
        #self.stridmake = self.make.lower()
        #self.stridmodel = self.vehiclemodel.lower()
        repeated = False
        for i in MakeModel.objects.all():
            if self != i:
                if str(self.make.lower()) == str(i.make.lower()) and str(self.vehiclemodel.lower()) == str(i.vehiclemodel.lower()):
                    self.make = i.make
                    self.vehiclemodel = i.vehiclemodel
                    self.id = i.id
                    repeated = True
                    break
                elif str(self.make.lower()) == str(i.make.lower()) and not(str(self.vehiclemodel.lower()) == str(i.vehiclemodel.lower())):
                    self.make = i.make
                elif str(self.vehiclemodel.lower()) == str(i.vehiclemodel.lower()) and not(str(self.make.lower()) == str(i.make.lower())):
                    self.vehiclemodel = i.vehiclemodel
        self.makemodel = str(self.make) + ' ' + str(self.vehiclemodel)
        if repeated == False:
            return super(MakeModel, self).save(*args, **kwargs)
    def __str__(self):
        accum = str(self.id)
        if self.makemodel != '':
            accum = str(self.makemodel)
        return accum

'''
class VehicleModel(models.Model):
    vehiclemodel = models.CharField(max_length=100)
    strid = models.CharField(max_length=100)
    def save(self, *args, **kwargs):
        repeated = False
        self.strid = self.trim.lower()
        for i in VehicleModel.objects.all():
            if str(self.strid) == str(i.strid):
                self.vehiclemodel = i.vehiclemodel
                repeated = True
                break
        if repeated == False:
            return super(VehicleModel, self).save(*args, **kwargs)
    def __str__(self):
        return str(self.vehiclemodel)
'''

class Trim(models.Model):
    trim = models.CharField('Trim',max_length=100)
    def save(self, *args, **kwargs):
        repeated = False
        for i in Trim.objects.all():
            if str(self.trim.lower()) == str(i.trim.lower()):
                self.trim = i.trim
                self.id = i.id
                repeated = True
                break
        if repeated == False:
            return super(Trim, self).save(*args, **kwargs)
    def __str__(self):
        return str(self.trim)
    
class EngineSize(models.Model):
    enginesize = models.CharField('Engine Size',max_length=100)
    def save(self, *args, **kwargs):
        repeated = False
        for i in EngineSize.objects.all():
            if str(self.enginesize) == str(i.enginesize):
                self.enginesize = i.enginesize
                self.id = i.id
                repeated = True
                break
        if repeated == False:
            return super(EngineSize, self).save(*args, **kwargs)
    def __str__(self):
        return str(self.enginesize)

class EngineCode(models.Model):
    enginecode = models.CharField('Engine Code',max_length=100)
    def save(self, *args, **kwargs):
        repeated = False
        for i in EngineCode.objects.all():
            if str(self.enginecode) == str(i.enginecode):
                self.enginecode = i.enginecode
                self.id = i.id
                repeated = True
                break
        if repeated == False:
            return super(EngineCode, self).save(*args, **kwargs)
    def __str__(self):
        return str(self.enginecode)

class Vehicle(models.Model):
    vehicle = models.TextField(max_length=50)
    #vehicle_year = models.ManyToManyField(Year,related_name='vehicle_year',default=datetime.datetime.now().year)
    vehicle_makemodel = models.ForeignKey(MakeModel,default='',verbose_name="Make and Model",on_delete=models.CASCADE)
    #vehicle_make = models.ManyToManyField(Make,related_name='vehicle_make',default='')
    #vehicle_vehiclemodel = models.ManyToManyField(VehicleModel,related_name='vehicle_vehiclemodel',default='')
    vehicle_trim = models.ForeignKey(Trim,default='',verbose_name="Trim",on_delete=models.CASCADE,null=True,blank=True)
    vehicle_enginesize = models.ForeignKey(EngineSize,default='',verbose_name="Engine Size",on_delete=models.CASCADE,null=True,blank=True)
    vehicle_enginecode = models.ForeignKey(EngineCode,default='',verbose_name="Engine Code",on_delete=models.CASCADE,null=True,blank=True)
    #vehicle_trim = models.ForeignKey(Trim,default='',on_delete=models.CASCADE)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    YEAR_CHOICES = []
    for r in range(1980, (datetime.datetime.now().year+1)):
        YEAR_CHOICES.append((r,r))
    year = models.IntegerField(choices=YEAR_CHOICES,default=datetime.datetime.now().year)

    transmission_type = models.CharField(max_length=1,choices=[('u','--'),('a','Auto'),('m','Manual'),],default='a')
    drive_wheel = models.CharField(max_length=1,choices=[('u','--'),('f','Front'),('r','Rear'),('a','AWD'),('4','4x4'),('t','Trailer'),],default='f')
    rear_brake_style = models.CharField(max_length=2,choices=[('uk','--'),('di','Disk'),('dr','Drum'),],default='di')
    e_brake_style = models.CharField(max_length=1,choices=[('u','--'),('m','Mechanical'),('e','Electrical'),],default='m')
    brake_note = models.TextField('Brake notes',max_length=200,blank=True)
    power_steering_type = models.CharField(max_length=1,choices=[('u','--'),('h','Hydraulic'),('e','Electrical')],default='h')
    absys = models.CharField('ABS',max_length=1,choices=[('u','--'),('y','Yes'),('n','No')],default='u')
    tpms = models.CharField('TPMS',max_length=1,choices=[('u','--'),('y','Yes'),('n','No')],default='u')
    ac = models.CharField('AC',max_length=1,choices=[('u','--'),('y','Yes'),('n','No')],default='u')
    tire_size_prefix = models.CharField(max_length=2,choices=[('u','Custom'),('',''),('LT','LT'),('P','P')],default='',blank=True)
    tire_size = models.CharField(max_length=15,blank=True)
    comments = models.TextField(max_length=200,blank=True)
    
    def save(self,*args,**kwargs):
        if self.tire_size_prefix != 'u':
            self.tire_size = ''.join(e for e in self.tire_size if e.isdigit())
            #print(self.tire_size)
            self.tire_size = str(self.tire_size_prefix) + str(self.tire_size)[:3] + '/' + str(self.tire_size)[3:5] + 'R' + str(self.tire_size)[5:]
        #print(str(self.year))
        accum = str(self.year) + ' '
        #print(self.vehicle_makemodel)
        if self.vehicle_makemodel != None:
            accum += str(self.vehicle_makemodel.__str__())
        #print(accum)
        self.vehicle = accum
        return super(Vehicle, self).save(*args, **kwargs)
    def __str__(self):
        accum = str(self.year) + ' '
        if self.vehicle_makemodel != None:
            accum += str(self.vehicle_makemodel.__str__())
        return accum
        #return str(self.year) + ' ' #+ str(self.vehicle_makemodel.all()[:1].get().__str__())