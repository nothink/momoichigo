"""momoichigo admin."""

from django.contrib import admin

from momoichigo.app.models import Resource

# Register your models here.
admin.site.register(Resource)
