from django.contrib import admin

from preferences.admin import PreferencesAdmin
from .models import GlobalPreference

class GlobalPreferencesAdmin(PreferencesAdmin):
    exclude = ('sites',)
    def has_add_permission(self, request): 
        return False
admin.site.register(GlobalPreference, GlobalPreferencesAdmin)