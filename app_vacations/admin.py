from django.contrib import admin
from .models import Vacation, Users, VacationType, Test, Answers, Expenses, Budget, VacancyCount, Response, Plans


admin.site.register(Vacation)
admin.site.register(Users)
admin.site.register(VacationType)
admin.site.register(Test)
admin.site.register(Answers)


@admin.register(VacancyCount)
class VacancyCountAdmin(admin.ModelAdmin):
    list_display = ('date', 'count')
    readonly_fields = ('date', 'count')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Expenses)
class ExpensesAdmin(admin.ModelAdmin):
    list_display = ('date', 'amount1', 'description1', 'amount2', 'description2', 'amount3', 'description3', 'amount4', 'description4', 'amount5', 'description5', 'total')
    readonly_fields = ('total',)


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('date', 'total')
    readonly_fields = ('date', 'total')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('name', 'hh_uz', 'olx_uz', 'telegram', 'recommend', 'total_dashboard')
    readonly_fields = ('total_dashboard',)


@admin.register(Plans)
class PlansAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'price', 'bonus', 'month', 'total')
    readonly_fields = ('total',)
