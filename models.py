from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta, date

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    transaction_type = models.CharField(max_length=10, choices=[('income', 'Income'), ('expense', 'Expense')])
    date = models.DateField(default=date.today)
    description = models.CharField(max_length=255)
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, blank=True, null=True)
    is_income = models.BooleanField(default=False)  
    next_due_date = models.DateField(blank=True, null=True)
    is_automated = models.BooleanField(default=False) 

    def save(self, *args, **kwargs):
        if self.frequency and not self.next_due_date:
            self.next_due_date = self.calculate_next_due_date()
        super().save(*args, **kwargs)

    def calculate_next_due_date(self):
        if not self.date:
            return None  # Safeguard if date is somehow unset
        
        # Calculate the next due date based on frequency
        if self.frequency == 'daily':
            return self.date + timedelta(days=1)
        elif self.frequency == 'monthly':
            return self.date + timedelta(days=30)
        elif self.frequency == 'quarterly':
            return self.date + timedelta(days=90)
        elif self.frequency == 'yearly':
            return self.date + timedelta(days=365)
        return None

# Django Signal to create default categories after migrations
@receiver(post_migrate)
def create_default_categories(sender, **kwargs):
    categories = ['Groceries', 'Rent', 'Utilities', 'Income', 'Savings']
    for category in categories:
        Category.objects.get_or_create(name=category)