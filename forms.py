from django import forms
from .models import Income, Expense, Budget, SavingsGoal

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['amount', 'source', 'date_received', 'description']

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'category', 'date_spent', 'description', 'is_recurring', 'recurrence_frequency']

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'limit', 'start_date', 'end_date']

class SavingsGoalForm(forms.ModelForm):
    class Meta:
        model = SavingsGoal
        fields = ['goal_name', 'target_amount', 'current_amount', 'target_date']
