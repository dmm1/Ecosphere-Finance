from django.contrib import admin
from finance.models import Category
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('description', 'amount', 'transaction_type', 'frequency', 'date', 'next_due_date', 'user')
    list_filter = ('transaction_type', 'frequency', 'date', 'category')
    search_fields = ('description', 'user__username')
    date_hierarchy = 'date'
    ordering = ('-date',)
    fieldsets = (
        (None, {
            'fields': ('user', 'amount', 'description', 'transaction_type', 'frequency', 'date', 'next_due_date', 'category')
        }),
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)