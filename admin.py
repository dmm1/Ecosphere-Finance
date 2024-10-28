from django.contrib import admin
from .models import Income, Expense, Budget, SavingsGoal

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ['amount', 'source', 'date_received', 'description']
    search_fields = ['source']

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['amount', 'category', 'date_spent', 'is_recurring', 'recurrence_frequency', 'next_due_date']
    search_fields = ['category']
    list_filter = ['is_recurring', 'recurrence_frequency']

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['category', 'limit', 'start_date', 'end_date']
    search_fields = ['category']

@admin.register(SavingsGoal)
class SavingsGoalAdmin(admin.ModelAdmin):
    list_display = ['goal_name', 'target_amount', 'current_amount', 'target_date']
    search_fields = ['goal_name']
