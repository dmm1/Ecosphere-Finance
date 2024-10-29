from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.db import transaction
from .models import Transaction

def get_next_due_date(current_date, frequency):
    """
    Calculate the next due date based on frequency from a given date.
    Uses relativedelta for accurate month/year calculations.
    """
    if frequency == 'daily':
        return current_date + timedelta(days=1)
    elif frequency == 'monthly':
        return current_date + relativedelta(months=1)
    elif frequency == 'quarterly':
        return current_date + relativedelta(months=3)
    elif frequency == 'yearly':
        return current_date + relativedelta(years=1)
    return None

def update_recurring_expenses():
    """
    Updates recurring transactions and creates automated entries.
    """
    today = timezone.now().date()
    
    # Get all recurring transactions
    recurring_transactions = Transaction.objects.filter(
        next_due_date__isnull=False,
        frequency__isnull=False
    ).select_for_update()

    with transaction.atomic():
        for recurring_tx in recurring_transactions:
            next_due = recurring_tx.next_due_date
            
            # Skip if next due date is in the future
            if next_due > today:
                continue
                
            while next_due <= today:
                # Check if transaction already exists for this date
                existing_tx = Transaction.objects.filter(
                    user=recurring_tx.user,
                    transaction_type=recurring_tx.transaction_type,
                    amount=recurring_tx.amount,
                    category=recurring_tx.category,
                    date=next_due,
                    is_automated=True
                ).exists()
                
                if not existing_tx:
                    # Create new transaction for this due date
                    Transaction.objects.create(
                        user=recurring_tx.user,
                        transaction_type=recurring_tx.transaction_type,
                        amount=recurring_tx.amount,
                        category=recurring_tx.category,
                        description=f"Automated: {recurring_tx.description}",
                        date=next_due,
                        is_automated=True
                    )
                
                # Calculate next due date
                next_due = get_next_due_date(next_due, recurring_tx.frequency)
                
            # Update the original recurring transaction's next due date
            recurring_tx.next_due_date = next_due
            recurring_tx.save()

def get_upcoming_transactions(user, days_ahead=30):
    """
    Get upcoming transactions for the next specified number of days.
    Returns separate querysets for income and expenses.
    """
    today = timezone.now().date()
    end_date = today + timedelta(days=days_ahead)
    
    base_query = Transaction.objects.filter(
        user=user,
        next_due_date__isnull=False,
        frequency__isnull=False,
        next_due_date__gte=today,
        next_due_date__lte=end_date
    )
    
    upcoming_income = base_query.filter(
        transaction_type='income'
    ).order_by('next_due_date')
    
    upcoming_expenses = base_query.filter(
        transaction_type='expense'
    ).order_by('next_due_date')
    
    return upcoming_income, upcoming_expenses