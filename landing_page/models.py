from django.db import models
from preferences.models import Preferences

class GlobalPreference(Preferences):
    labour_markup = models.FloatField(default=1.0)
    labour_rate = models.FloatField(default=1.0)