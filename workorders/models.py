from django.db import models
from clientcars_db.models import Client
from contacts_db.models import Contact
from sup_invoices.models import Part
from datetime import datetime
from django.utils.timezone import now

# Create your models here.
class Estimation(models.Model):
    def number():
        no = Estimation.objects.count()
        if no == None:
            return 1
        else:
            return no + 1
    estimation = models.IntegerField(unique=True, default=number)

    client = models.ForeignKey(Client,on_delete=models.SET_NULL,blank=True,null=True)
    def __str__(self):
        return str(self.estimation)
    class meta:
        verbose_name = "Estimation"

class EstimationLine(models.Model):
    order = models.ForeignKey(Estimation,on_delete=models.CASCADE,verbose_name = "Estimation")
    technician = models.ForeignKey(Contact,on_delete=models.SET_NULL,blank=True,null=True)
    #technician = models.CharField(max_length=50,blank=True,null=True)
    customer_comments = models.TextField(max_length=200,blank=True,null=True)
    technician_comments = models.TextField(max_length=200,blank=True,null=True)
    test_results = models.TextField(max_length=200,blank=True,null=True)
    internal_comments = models.TextField(max_length=200,blank=True,null=True)
    hours_charged = models.FloatField(default=0.0)
    labour_guide = models.FloatField('Labour Guide Hours',default=0.0)
    labour_charged = models.FloatField("Labour Charged ($)",default=0.0,)
    parts = models.ManyToManyField(Part,related_name='estimationline',related_query_name='estimationline',through='LineParts',blank=True)
    date = models.DateTimeField(default=now)

'''
class EstimationParts(models.Model):
    estimationline = models.ForeignKey(EstimationLine,on_delete=models.CASCADE)
    part = models.ForeignKey(Part,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
'''

class WorkOrder(models.Model):
    def number():
        no = WorkOrder.objects.count()
        if no == None:
            return 1
        else:
            return no + 1
    workorder = models.CharField(max_length=200,unique=True, default=number)

    client = models.ForeignKey(Client,on_delete=models.SET_NULL,blank=True,null=True)
    def __str__(self):
        return str(self.workorder)
    class meta:
        verbose_name = "Work Order"

class WorkOrderLine(models.Model):
    order = models.ForeignKey(WorkOrder,on_delete=models.CASCADE,verbose_name = "Work Order")
    technician = models.ForeignKey(Contact,on_delete=models.SET_NULL,blank=True,null=True)
    #technician = models.CharField(max_length=50,blank=True,null=True)
    customer_comments = models.TextField(max_length=200,blank=True,null=True)
    technician_comments = models.TextField(max_length=200,blank=True,null=True)
    test_results = models.TextField(max_length=200,blank=True,null=True)
    internal_comments = models.TextField(max_length=200,blank=True,null=True)
    hours_charged = models.FloatField(default=0.0)
    labour_guide = models.FloatField('Labour Guide Hours',default=0.0)
    labour_charged = models.FloatField("Labour Charged ($)",default=0.0,)
    parts = models.ManyToManyField(Part,related_name='workorderline',related_query_name='workorderline',through='LineParts',blank=True)
    status = models.CharField(max_length=1,choices=[('c','Cancelled'),('o','Ongoing'),('d','Completed'),],default='o')
    date = models.DateTimeField(default=now)
    def save(self,*args,**kwargs):
        from stock.models import InventoryPart
        #self.hours_charged = self.labour_guide * global_preferences_registry.manager()['workorder__labour_markup']
        instance = super(WorkOrderLine, self).save(*args, **kwargs)
        parts = self.parts.all()
        for part in parts:
            try:
                invpart = InventoryPart.objects.get(sup_part=part)
                invpart.save()
            except:
                pass
        return instance

'''
class WorkOrderParts(models.Model):
    workorderline = models.ForeignKey(WorkOrderLine,on_delete=models.CASCADE)
    part = models.ForeignKey(Part,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    def save(self,*args,**kwargs):
        from stock.models import InventoryPart
        instance = super(WorkOrderParts, self).save(*args, **kwargs)
        print(InventoryPart.objects.get(sup_part=self.part))
        try:
            invpart = InventoryPart.objects.get(sup_part=self.part)
            print(invpart)
            invpart.save()
        except:
            pass
        return instance
'''

class Invoice(models.Model):
    def number():
        no = Invoice.objects.count()
        if no == None:
            return 1
        else:
            return no + 1
    invoice = models.IntegerField(unique=True, default=number)

    client = models.ForeignKey(Client,on_delete=models.SET_NULL,blank=True,null=True)
    def __str__(self):
        return str(self.invoice)
    class meta:
        verbose_name = "Invoice"

class InvoiceLine(models.Model):
    order = models.ForeignKey(Invoice,on_delete=models.CASCADE,verbose_name = "Invoice")
    technician = models.ForeignKey(Contact,on_delete=models.SET_NULL,blank=True,null=True)
    #technician = models.CharField(max_length=50,blank=True,null=True)
    customer_comments = models.TextField(max_length=200,blank=True,null=True)
    technician_comments = models.TextField(max_length=200,blank=True,null=True)
    test_results = models.TextField(max_length=200,blank=True,null=True)
    internal_comments = models.TextField(max_length=200,blank=True,null=True)
    hours_charged = models.FloatField(default=0.0)
    labour_guide = models.FloatField('Labour Guide Hours',default=0.0)
    labour_charged = models.FloatField("Labour Charged ($)",default=0.0,)
    parts = models.ManyToManyField(Part,related_name='invoiceline',related_query_name='invoiceline',through='LineParts',blank=True)
    status = models.CharField(max_length=1,choices=[('b','Billed'),('p','Paid'),],default='b')
    date = models.DateTimeField(default=now)

'''
class InvoiceParts(models.Model):
    invoiceline = models.ForeignKey(InvoiceLine,on_delete=models.CASCADE)
    part = models.ForeignKey(Part,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
'''

class LineParts(models.Model):
    estimationline = models.ForeignKey(EstimationLine,on_delete=models.CASCADE,null=True)
    workorderline = models.ForeignKey(WorkOrderLine,on_delete=models.CASCADE,null=True)
    invoiceline = models.ForeignKey(InvoiceLine,on_delete=models.CASCADE,null=True)
    part = models.ForeignKey(Part,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    def save(self,*args,**kwargs):
        from stock.models import InventoryPart
        instance = super(LineParts, self).save(*args, **kwargs)
        if self.workorderline != None:
            try:
                invpart = InventoryPart.objects.get(sup_part=self.part)
                #print(invpart)
                invpart.save()
            except:
                pass
        return instance