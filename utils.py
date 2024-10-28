# utils.py
from .models import Transaction
from datetime import date

def update_recurring_expenses():
    today = date.today()
    recurring_transactions = Transaction.objects.filter(next_due_date__lte=today)

    for transaction in recurring_transactions:
        transaction.update_next_due_date()
