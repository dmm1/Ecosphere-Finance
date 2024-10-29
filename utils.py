from datetime import timedelta
from django.utils import timezone
from .models import Transaction

def update_recurring_expenses():
    recurring_transactions = Transaction.objects.filter(next_due_date__isnull=False)

    for transaction in recurring_transactions:
        # Calculate the next due date based on frequency
        if transaction.frequency == 'daily':
            next_due_date = transaction.next_due_date + timedelta(days=1)
        elif transaction.frequency == 'monthly':
            next_due_date = transaction.next_due_date + timedelta(weeks=4)  # Roughly one month
        elif transaction.frequency == 'quarterly':
            next_due_date = transaction.next_due_date + timedelta(weeks=13)  # Roughly three months
        elif transaction.frequency == 'yearly':
            next_due_date = transaction.next_due_date + timedelta(weeks=52)  # Roughly one year
        else:
            continue  # Skip if no valid frequency

        # Check if today's date matches or is greater than the next due date
        if timezone.now().date() >= transaction.next_due_date:
            # Check if a transaction with the same parameters already exists
            if not Transaction.objects.filter(
                user=transaction.user,
                transaction_type=transaction.transaction_type,
                category=transaction.category,
                next_due_date=next_due_date,
                is_automated=True  # Only check for automated transactions
            ).exists():
                # Create a new transaction instance
                new_transaction = Transaction(
                    user=transaction.user,
                    transaction_type=transaction.transaction_type,
                    amount=transaction.amount,
                    category=transaction.category,
                    description=f"Created because of frequency of '{transaction.description}'",  # Correct description
                    next_due_date=next_due_date,
                    frequency=transaction.frequency,
                    is_automated=True,  # Mark as automated
                )
                new_transaction.save()

                # Update the existing transaction's next_due_date
                transaction.next_due_date = next_due_date
                transaction.save()
