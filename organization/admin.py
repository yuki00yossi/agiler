from django.contrib import admin
from .models import OrganizationUser, Organization
# Register your models here.
admin.site.register(OrganizationUser)
admin.site.register(Organization)
