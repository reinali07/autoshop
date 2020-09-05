from django.contrib import admin
from .models import Business, Contact, PhoneNumber, Email, SocialMedia
from .filters import *
from .inlines import *
#from contacts_db.inlines import ContactInline
from django.utils.html import format_html

# Register your models here.

class ContactAdmin(admin.ModelAdmin):
    inlines = [
        BusinessInline,
        PhoneInline,
        EmailInline,
        SocialInline,
        #ClientInline,
        #ContactInline,
    ]
    search_fields = ['first_name','last_name','nickname',]
    ordering = ['last_name']
    exclude = ('businesses','contact',)
    fieldsets = [
        (None,               {'fields': [('first_name','last_name'),('is_tech',),('nickname','image',),'discount_rate','comments',]}),
    ]
    #filter_horizontal = ('businesses',)
    def delete_contact(self, obj):
        return format_html('<a class="btn" href="/admin/contacts_db/contact/{}/delete/">Delete</a>', obj.id)
    def disp_img(self,obj):
        #src = 'images/contacts/people/{0}-{1}.{2}'.format(obj.first_name, obj.last_name,format)
        if obj.image != None:
            img = format_html('<div style="width:80px;height:80px;"><img src="{}" style="max-width:100%;max-height:100%;"></div>',obj.image.url)
        else:
            img = format_html('<div style="width:80px;height:80px;"><img src="{% static \'admin/contacts_db/contact/img/no-image.jpg\' %}" style="max-width:100%;max-height:100%;"></div>')
        return img
    def last_first(self):
        return str(self.last_name) + ', ' + str(self.first_name) 
    list_display = ['disp_img',last_first,'nickname','delete_contact']
    #list_filter = ['last_name','businesses__business']
    list_filter = [NameFilter,BusinessFilter,EmailFilter,PhoneFilter,SocialFilter,]
    #search_fields = ['first_name','last_name','nickname','businesses__business','phones__phone_number','phones__phone_type','emails__email_address','socials__platform','socials__social_handle','businesses__phones__phone_number','businesses__phones__phone_type','businesses__emails__email_address','businesses__socials__platform','business__socials__social_handle',]
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        #print(queryset.filter(internal=None))
        #print(request.GET['field_name'])
        #print(request.GET)
        try:
            if 'lineparts_set' in request.GET['field_name']:
                queryset = queryset.filter(is_tech=True)
        except:
            pass
        return queryset, use_distinct

class BusinessAdmin(admin.ModelAdmin):
    inlines = [
        BusinessInline,
        PhoneInline,
        EmailInline,
        SocialInline,
        #ClientInline,
    ]
    fieldsets = [
        (None,               {'fields': [('business','business_type'),'image','discount_rate','comments']}),
    ]
    search_fields = ['business']
    ordering = ['business']
    list_filter = [BusinessNameFilter,PersonNameFilter,EmailFilter,PhoneFilter,SocialFilter,]
    list_display = ['disp_img','business','delete_contact']
    #fieldsets = [
    #    (None,               {'fields': ['business_name','business_type',]}),
    #]
    #filter_horizontal = ('businesses',)
    def delete_contact(self, obj):
        return format_html('<a class="btn" href="/admin/contacts_db/contact/{}/delete/">Delete</a>', obj.id)
    def disp_img(self,obj):
        #src = 'images/contacts/people/{0}-{1}.{2}'.format(obj.first_name, obj.last_name,format)
        if obj.image != None:
            img = format_html('<div style="width:80px;height:80px;"><img src="{}" style="max-width:100%;max-height:100%;"></div>',obj.image.url)
        else:
            img = format_html('<div style="width:80px;height:80px;"><img src="{% static \'admin/contacts_db/business/img/no-image.jpg\' %}" style="max-width:100%;max-height:100%;"></div>')
        return img

class HideAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}

admin.site.register(Contact, ContactAdmin)
admin.site.register(Business, BusinessAdmin)
admin.site.register(PhoneNumber,HideAdmin)
admin.site.register(Email,HideAdmin)
admin.site.register(SocialMedia,HideAdmin)