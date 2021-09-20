from django.contrib import admin

# Register your models here.
from users.models import PortalUser, DoctorSpeciality, Doctor

admin.site.register(PortalUser)
admin.site.register(Doctor)
admin.site.register(DoctorSpeciality)
