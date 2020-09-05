from django.contrib import admin
from .models import *
from .inlines import *
from .filters import *
from django.utils.html import format_html

# Register your models here.

#@admin.register(Client)
#@admin_thumbnails.thumbnail('image','Thumbnail')
class ClientAdmin(admin.ModelAdmin):
    #inlines = [
    #    ContactInline,
        #VehicleInline,
    #]
    #search_fields = ['vin','licenseplate',]
    fieldsets = [
        (None,               {'fields': ['vin','licenseplate','colour','clientvehicle','clientcontact','image',]}),
        ('Comments',         {'fields': ['comments',]}),
    ]
    #inlines = [VehicleInline,]
    autocomplete_fields = ['clientcontact','clientvehicle',]
    def disp_img(self,obj):
        #src = 'images/contacts/people/{0}-{1}.{2}'.format(obj.first_name, obj.last_name,format)
        if obj.image != None:
            img = format_html('<div style="width:80px;height:80px;"><img src="{}" style="max-width:100%;max-height:100%;"></div>',obj.image.url)
        else:
            img = format_html('<div style="width:80px;height:80px;"><img src="{% static \'admin/contacts_db/business/img/no-image.jpg\' %}" style="max-width:100%;max-height:100%;"></div>')
        return img

    def delete_car(self, obj):
        return format_html('<a class="btn" href="/admin/clientcars_db/client/{}/delete/">Delete</a>', obj.id)
    def last_first(self):
        return str(self.clientcontact.last_name) + ', ' + str(self.clientcontact.first_name)
    def phone_number(self):
        return str(self.clientcontact.phones.all()[:1].get().phonenumber)
    def vehicle_name(self):
        return str(self.clientvehicle.__str__()) 
    search_fields = ('clientcontact','clientvehicle','vin','licenseplate',)
    list_display = ['disp_img',last_first,vehicle_name,'licenseplate',phone_number,'delete_car']
    list_filter = [VINFilter,LicenseFilter,ColourFilter,MakeModelFilter,CommentFilter,PersonNameFilter,BusinessFilter,PhoneFilter,EmailFilter,SocialFilter,]
    #exclude = ['clientcontact',]
    #autocomplete_fields = ['contact','vehicle',]

#class ClientAdmin(ReverseModelAdmin):
#    inline_type = 'tabular'
#    inline_reverse = ['contact',
#                      ('contact', {'fields': ['first_name']}),
#                      ]
admin.site.register(Client,ClientAdmin)