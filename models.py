from django.db import models
from django.utils import timezone
from datetime import timedelta
from dateutil.relativedelta import relativedelta


class Income(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    source = models.CharField(max_length=255)
    date_received = models.DateField()
    description = models.TextField(blank=True, null=True)

class Expense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=255)
    date_spent = models.DateField()
    description = models.TextField(blank=True, null=True)
    is_recurring = models.BooleanField(default=False)
    recurrence_frequency = models.CharField(
        max_length=50,
        choices=[
            ('daily', 'Täglich'),
            ('weekly', 'Wöchentlich'),
            ('monthly', 'Monatlich'),
            ('quarterly', 'Quartalsweise'),
            ('semiannually', 'Halbjährlich'),
            ('yearly', 'Jährlich')
        ],
        blank=True,
        null=True
    )
    next_due_date = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.is_recurring and not self.next_due_date:
            self.next_due_date = self.calculate_next_due_date()
        super().save(*args, **kwargs)

    def calculate_next_due_date(self):
        if self.recurrence_frequency == 'daily':
            return self.date_spent + timedelta(days=1)
        elif self.recurrence_frequency == 'weekly':
            return self.date_spent + timedelta(weeks=1)
        elif self.recurrence_frequency == 'monthly':
            return self.date_spent + relativedelta(months=1)
        elif self.recurrence_frequency == 'quarterly':
            return self.date_spent + relativedelta(months=3)
        elif self.recurrence_frequency == 'semiannually':
            return self.date_spent + relativedelta(months=6)
        elif self.recurrence_frequency == 'yearly':
            return self.date_spent + relativedelta(years=1)
        return None

class Budget(models.Model):
    category = models.CharField(max_length=255)
    limit = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

class SavingsGoal(models.Model):
    goal_name = models.CharField(max_length=255)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    target_date = models.DateField()
