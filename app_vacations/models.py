from django.db import models


# Create your models here.
class VacationType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Vacancy Types"
        verbose_name = "Vacancy Type"
        db_table = "vacation_type"


class Vacation(models.Model):
    image_uz = models.ImageField(upload_to='media', null=True, blank=True)
    image_ru = models.ImageField(upload_to='media', null=True, blank=True)
    name_uz = models.CharField(max_length=100)
    name_ru = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    contacts1 = models.CharField(max_length=100, null=False, blank=False)
    contacts2 = models.CharField(max_length=100, null=True, blank=True)
    location_uz = models.CharField(max_length=100)
    location_ru = models.CharField(max_length=100)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    requirements_uz = models.TextField()
    requirements_ru = models.TextField()
    amenities_uz = models.TextField()
    amenities_ru = models.TextField()
    salary = models.CharField(max_length=20)
    experience = models.CharField(max_length=10)
    vacation = models.ForeignKey(VacationType, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name_uz

    class Meta:
        db_table = 'vacation'
        verbose_name = 'Vacancy'
        verbose_name_plural = 'Vacancies'


class Users(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    birth_date = models.DateField()
    city = models.CharField(max_length=100)
    education = models.CharField(max_length=100)
    languages = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} {self.surname}"

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'