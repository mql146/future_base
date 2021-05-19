from django.contrib import admin

from .models import Provision

# Register your models here.

class provision_admin(admin.ModelAdmin):
    pass

admin.site.register(Provision,provision_admin)
