from django.contrib import admin
from .models import Vacation, Users, VacationType, Test, Answers

# Register your models here.
admin.site.register(Vacation)
admin.site.register(Users)
admin.site.register(VacationType)
admin.site.register(Test)
admin.site.register(Answers)