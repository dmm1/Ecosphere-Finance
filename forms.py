# forms.py
from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'description', 'transaction_type', 'frequency', 'date', 'category', 'next_due_date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'frequency': forms.Select(choices=Transaction.FREQUENCY_CHOICES),
        }
        labels = {
            'amount': 'Amount',
            'description': 'Description',
            'transaction_type': 'Type',
            'frequency': 'Frequency',
            'date': 'Date',
            'category': 'Category',
            'next_due_date': 'Next Due Date',
        }

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError("Amount must be positive.")
        return amount
