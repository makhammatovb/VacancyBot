from django.contrib import admin
from .models import Vacation, Users, VacationType

# Register your models here.
admin.site.register(Vacation)
admin.site.register(Users)
admin.site.register(VacationType)