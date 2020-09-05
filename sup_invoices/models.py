from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from contacts_db.models import Business
import datetime
#from model_clone import CloneMixin
#from django.core.exceptions import ValidationError
#from stock.models import InventoryPart
import uuid
#from django.db import transaction

# Create your models here.

class Part(models.Model):
    part = models.CharField(max_length=80)
    part_number = models.CharField('Part Number',max_length=30)
    #internal_part = models.CharField('Internal Part Number',max_length=30) #make this a foreign key later
    #stock_part = models.ForeignKey(InventoryPart,on_delete=models.SET_NULL,blank=True,null=True)
    description = models.CharField(max_length=50,blank=True)
    brand = models.CharField(max_length=50)
    quantity = models.IntegerField('Stock',default=0)
    #internal = models.ForeignKey(InventoryPart,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Inventory Part')
    class Meta:
        unique_together = ('part_number', 'brand',)
        ordering = ['-id']
    #price = models.FloatField()
    def save(self,*args,**kwargs):
        self.part = self.brand + ': ' + self.part_number + ' '
        self.part += ''.join(e for e in self.part_number if e.isalnum())
        
        invoices = self.supplierinvoiceparts_set.all().exclude(supplier_invoice__is_return=True)
        workorders = self.lineparts_set.all().exclude(workorderline__status='c')
        accum = 0
        for invoice in invoices:
            accum += invoice.quantity - invoice.returnedqty
        for workorder in workorders:
            accum -= workorder.quantity

        #self.internal_set.all()[:1].get().save()
        return super(Part,self).save(*args,**kwargs)
    def __str__(self):
        return str(self.brand) + ': ' + str(self.part_number) + ' '

#class SupplierInvoice(models.Model,CloneMixin):
class SupplierInvoice(models.Model):
    supplier_invoice = models.CharField('Invoice Number',max_length=20,validators=[RegexValidator(r'^\d{1,10}$', message="Invoice Number cannot contain non-numeric characters")],blank=False,null=False,unique=True)
    po = models.CharField('PO Number',max_length=20,validators=[RegexValidator(r'^\d{1,10}$', message="PO Number cannot contain non-numeric characters")])
    date = models.DateField(default=timezone.now,null=True,blank=True)
    supplier = models.ForeignKey(Business,max_length=40,on_delete=models.SET_NULL,null=True)
    is_return = models.BooleanField('Return?',default=False)
    purchased_parts = models.ManyToManyField(Part,related_name='purchased_parts',through='SupplierInvoiceParts')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference = models.CharField('Reference Invoice Number',max_length=20,validators=[RegexValidator(r'^\d{1,10}$', message="Invoice Number cannot contain non-numeric characters")],blank=True)
    comments = models.TextField(max_length=100,blank=True)
    #_clone_model_fields = ('po','supplier','reference',)
    #_clone_many_to_many_fields = ('purchased_parts',)
    #make validation for retqty <= quantity - returnedqty
    '''
    def update_supplierinvoiceparts(self,*args,**kwargs):
        if not self.is_return:
            self.reference = self.supplier_invoice
            parts = self.purchased_parts.all()
            for part in parts:
                all_returns = SupplierInvoiceParts.objects.filter(supplier_invoice__reference=self.reference,part=part)
                original_invoice_link = SupplierInvoiceParts.objects.get(supplier_invoice=self,part=part)
                accum = 0
                for i in all_returns:
                    accum += i.retqty
                original_invoice_link.returnedqty = accum
                original_invoice_link.save()
                all_returns.update(returnedqty=original_invoice_link.returnedqty)
            return super(SupplierInvoiceParts,original_invoice_link).save(*args,**kwargs), super(SupplierInvoice,self).save(*args,**kwargs)
        else:
            parts = self.purchased_parts.all()
            for part in parts:
                original_invoice = SupplierInvoice.objects.get(supplier_invoice=self.reference)
                return original_invoice.update_supplierinvoiceparts()
    #def update_parts(self,*args,**kwargs):
        '''
    def save(self, *args, **kwargs):
        #instance = super(SupplierInvoice, self).save(*args, **kwargs)
        #temp = transaction.on_commit(self.update_supplierinvoiceparts)
        if not self.is_return:
            self.reference = self.supplier_invoice
        #print(self.reference)
        return super(SupplierInvoice, self).save(*args, **kwargs)
    def delete(self,*args, **kwargs):
        from stock.models import InventoryPart
        #instance = super(SupplierInvoice,self).delete(*args,**kwargs)
        partlinks = self.supplierinvoiceparts_set.all()
        for partlink in partlinks:
            accum = 0
            links = SupplierInvoiceParts.objects.filter(supplier_invoice__reference=self.reference,part=partlink.part).exclude(pk=partlink.pk)
            #print(links)
            for link in links.filter(supplier_invoice__is_return=True):
                accum += link.retqty
            #print(accum)
            links.update(returnedqty=accum)
            try:
                partlink.part.internal.save()
                #InventoryPart.objects.get(sup_part=partlink.part).save()
            except:
                pass
        if not self.is_return:
            for invoice in SupplierInvoice.objects.filter(reference=self.reference).exclude(pk=self.pk):
                super(SupplierInvoice,invoice).delete(*args,**kwargs)
        return super(SupplierInvoice,self).delete(*args,**kwargs)
    '''
    def delete(self,*args,**kwargs):
        #print('delete')
        if self.is_return:
            parts = self.purchased_parts.all()
            for part in parts:
                original_invoice_link = SupplierInvoiceParts.objects.get(supplier_invoice__supplier_invoice=self.reference,part=part)
                current_invoice_link = SupplierInvoiceParts.objects.get(supplier_invoice=self,part=part)
                original_invoice_link.returnedqty -= current_invoice_link.retqty
                original_invoice_link.save()
                #print(original_invoice_link.returnedqty)
        else:
            parts = self.purchased_parts.all()
            for part in parts:
                current_invoice_link = SupplierInvoiceParts.objects.get(supplier_invoice=self,part=part)
                internal = part.internal.all()[:1].get()
                #print(internal)
                internal.stock -= (current_invoice_link.quantity - current_invoice_link.returnedqty)
                internal.save()
                try:
                    SupplierInvoice.objects.exclude(id=self.id).filter(reference=self.supplier_invoice).delete()
                except:
                    pass
        return super(SupplierInvoice,self).delete(*args,**kwargs)
    '''
    def __str__(self):
        return str(self.supplier_invoice)
    class Meta:
        verbose_name = 'Supplier Invoice'

class Prices(models.Model):
    class Meta:
        verbose_name_plural = "Prices"
    def __str__(self):
        return str(self.id)
    history = models.ManyToManyField(Part,related_name='prices',through='SupplierInvoiceParts',blank=True)

class SupplierInvoiceParts(models.Model):
    prices = models.ForeignKey(Prices,on_delete=models.SET_NULL,null=True,blank=True)
    supplier_invoice = models.ForeignKey(SupplierInvoice,on_delete=models.CASCADE,null=True)
    part = models.ForeignKey(Part,on_delete=models.CASCADE,blank=False,null=False)
    quantity = models.PositiveIntegerField(default=1)
    returnedqty = models.PositiveIntegerField('Total returned',default=0,null=True,blank=True)
    retqty = models.PositiveIntegerField('Return Qty',null=True,blank=True,default=0)
    list_price = models.DecimalField(decimal_places=2,max_digits=7,blank=True,null=True)
    cost = models.DecimalField(decimal_places=2,max_digits=7)
    core = models.BooleanField('Core?',default=False)
    is_promo = models.BooleanField('Promotion?',default=False)
    package_size = models.FloatField(default=0)
    supplier = models.ForeignKey(Business,on_delete=models.CASCADE,blank=True,null=True)
    date = models.DateField(default=timezone.now)
    comments = models.TextField(max_length=50,blank=True)
    
    def save(self,*args,**kwargs):
        from stock.models import InventoryPart
        instance = super(SupplierInvoiceParts, self).save(*args, **kwargs)
        accum = 0
        links = SupplierInvoiceParts.objects.filter(supplier_invoice__reference=self.supplier_invoice.reference,part=self.part)
        for link in links.filter(supplier_invoice__is_return=True):
            accum += link.retqty
        #print(accum)
        links.update(returnedqty=accum)
        try:
            self.part.internal.save()
            #InventoryPart.objects.get(sup_part=self.part).save()
        except:
            pass
        return instance

    class Meta:
        verbose_name_plural = "Part Purchase History"

    def __str__(self):
        try:
            return '(PO: '+str(self.supplier_invoice.po) + ') ' + str(self.part.part)
        except:
            return str(self.part.part)
