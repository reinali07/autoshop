from django.db import models
from django.db import transaction
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.db.models import Q
from sup_invoices.models import Part

# Create your models here.
class InventoryPart(models.Model):
    part_number = models.CharField('Internal Part Number',primary_key=True,max_length=30)
    stock = models.IntegerField(blank=True,null=True)
    min_stock = models.PositiveIntegerField()
    full_stock = models.PositiveIntegerField()
    description = models.TextField(max_length=200,blank=True)
    average_price = models.DecimalField(decimal_places=2,max_digits=7,blank=True,null=True)
    area = models.CharField(max_length=20,blank=True)
    row = models.CharField(max_length=10,blank=True)
    line = models.CharField(max_length=10,blank=True)
    sup_part = models.ManyToManyField(Part,related_query_name='internal',related_name='internal',blank=True,verbose_name='part')
    interchangeable = models.CharField('Interchangeable Part',max_length=30,blank=True)
    standard_unit = models.CharField(max_length=10)

    def needs_restock(self):
        return "Needs Restock" if self.stock <= self.min_stock else "Stock OK"
    def update_sup_part(self,*args,**kwargs):
        from sup_invoices.models import Part, SupplierInvoiceParts
        from workorders.models import LineParts
        parts = self.sup_part.all()
        accum = 0
        avg = 0
        tally = 0
        for part in parts:
            #print(part)
            orders = SupplierInvoiceParts.objects.filter(part=part,supplier_invoice__is_return=False)
            workorders = LineParts.objects.filter(part=part).exclude(workorderline__status='c').exclude(workorderline=None)
            for order in orders:
                accum += order.quantity - order.returnedqty
                avg += float(order.cost)/float(order.package_size)
                tally += 1
                #print(accum)
            for workorder in workorders:
                #print('used',workorder.quantity)
                accum -= workorder.quantity
            part.quantity = accum
            #print(part.quantity)
            part.save()
        try:
            calc_average_price = avg/tally
        except:
            calc_average_price = 0
        self.average_price = calc_average_price
        self.stock = accum
        return super(InventoryPart, self).save(*args, **kwargs)
    def save(self, *args, **kwargs):
        instance = super(InventoryPart, self).save(*args, **kwargs)
        temp = transaction.on_commit(self.update_sup_part)
        #temp = self.update_sup_part()
        #print([calc_average_price,tallied_stock])
        #self.average_price = calc_average_price
        #self.stock = tallied_stock
        #super(InventoryPart, self).save(*args, **kwargs)
        return instance
        #return super(InventoryPart, self).save(*args, **kwargs)
    class Meta:
        verbose_name = 'Internal Part'
    def __str__(self):
        return str(self.part_number)
    
'''
@receiver(m2m_changed, sender=InventoryPart.sup_part.through)
def sup_parts_change(sender, action, pk_set, instance=None, **kwargs):
    if action in ['post_add', 'post_remove']:
        queryset = instance.sup_part.all()
        accum = 0
        avg = 0
        tally = 0
        for part in parts:
           orders = SupplierInvoiceParts.objects.filter(part=part)
           for order in orders:
               accum += order.quantity - order.returnedqty
               avg += order.list_price
               tally +=1
        try:
            instance.average_price = avg/tally
        except:
            instance.average_price = 0
        instance.stock = accum
        instance.save()
#class Prices(models.Model):
#    internal_part = models.ForeignKey(InventoryPart,on_delete=models.CASCADE)
#    purchased_part = models.OneToOneField(SupplierInvoicePart,on_delete=models.CASCADE)
'''
