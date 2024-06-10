from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum, F, Value, DecimalField
from django.db.models.functions import Coalesce
from .models import Expenses, Budget, Vacation, VacancyCount
from datetime import date


@receiver(post_save, sender=Expenses)
@receiver(post_delete, sender=Expenses)
def update_budget(sender, instance, **kwargs):
    expense_month = instance.date.replace(day=1)

    total = Expenses.objects.filter(date__year=expense_month.year, date__month=expense_month.month).aggregate(
        total_amount=Sum(
            Coalesce('amount1', Value(0), output_field=DecimalField()) +
            Coalesce('amount2', Value(0), output_field=DecimalField()) +
            Coalesce('amount3', Value(0), output_field=DecimalField()) +
            Coalesce('amount4', Value(0), output_field=DecimalField()) +
            Coalesce('amount5', Value(0), output_field=DecimalField()),
            output_field=DecimalField()
        )
    )['total_amount'] or 0

    Budget.objects.update_or_create(
        date=expense_month,
        defaults={'total': total}
    )


@receiver(post_save, sender=Vacation)
@receiver(post_delete, sender=Vacation)
def update_vacation_count(sender, instance, **kwargs):
    vacation_month = instance.start_date.replace(day=1)
    count = Vacation.objects.filter(start_date__year=vacation_month.year,
                                    start_date__month=vacation_month.month).count()

    VacancyCount.objects.update_or_create(
        date=vacation_month,
        defaults={'count': count}
    )
