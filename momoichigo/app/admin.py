"""momoichigo admin."""

from django.contrib import admin

from momoichigo.app import models

# Register your models here.
admin.site.register(models.ResourceQueue)
admin.site.register(models.Resource)
