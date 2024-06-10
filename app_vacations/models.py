from django.utils import timezone

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


class Test(models.Model):
    vacancy_type = models.ForeignKey(VacationType, on_delete=models.CASCADE)
    test_uz = models.TextField()
    test_ru = models.TextField()

    def __str__(self):
        return self.test_uz

    class Meta:
        db_table = 'test'
        verbose_name = 'Test'
        verbose_name_plural = 'Tests'


class Users(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    birth_date = models.DateField()
    city = models.CharField(max_length=100)
    education = models.CharField(max_length=100)
    languages = models.CharField(max_length=100)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, null=True, blank=True)
    answer_uz = models.TextField(null=True, blank=True)
    answer_ru = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} {self.surname}"

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Answers(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    answer_uz = models.TextField(null=True, blank=True)
    answer_ru = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.name} {self.user.surname}"

    class Meta:
        db_table = 'answers'
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'


class Expenses(models.Model):
    date = models.DateField(default=timezone.now)
    amount1 = models.DecimalField(max_digits=20, decimal_places=2)
    description1 = models.TextField()
    amount2 = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    description2 = models.TextField(null=True, blank=True)
    amount3 = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    description3 = models.TextField(null=True, blank=True)
    amount4 = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    description4 = models.TextField(null=True, blank=True)
    amount5 = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    description5 = models.TextField(null=True, blank=True)
    total = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.total = (self.amount1 or 0) + (self.amount2 or 0) + (self.amount3 or 0) + (self.amount4 or 0) + (self.amount5 or 0)
        super(Expenses, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.amount1} {self.description1}"

    class Meta:
        db_table = 'expenses'
        verbose_name = 'Expense'
        verbose_name_plural = 'Expenses'


class Budget(models.Model):
    date = models.DateField(unique=True)
    total = models.DecimalField(max_digits=30, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.date.strftime('%B %Y')}: {self.total}"

    class Meta:
        db_table = 'budget'
        verbose_name = 'Budget'


class VacancyCount(models.Model):
    date = models.DateField(unique=True)
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.date} {self.count}"

    class Meta:
        db_table = 'vacancy_count'
        verbose_name = 'Vacancy Count'
        verbose_name_plural = 'Vacancies Count'


class Response(models.Model):
    name = models.CharField(max_length=200)
    hh_uz = models.PositiveIntegerField(default=0)
    olx_uz = models.PositiveIntegerField(default=0)
    telegram = models.PositiveIntegerField(default=0)
    recommend = models.PositiveIntegerField(default=0)
    total_dashboard = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        self.total_dashboard = self.hh_uz + self.olx_uz + self.telegram + self.recommend
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'response'
        verbose_name = 'Response'
        verbose_name_plural = 'Responses'


class Plans(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    bonus = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    month = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=20, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total = self.price + self.bonus + self.month
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'plans'
        verbose_name = 'Plan'
        verbose_name_plural = 'Plans'
