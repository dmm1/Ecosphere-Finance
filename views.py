from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Income, Expense, Budget, SavingsGoal
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.db.models import Sum
from django.db.models.functions import TruncMonth
import json
from datetime import timedelta

def dashboard(request):
    """Render the dashboard page and update recurring expenses."""
    update_recurring_expenses(request)
    return render(request, 'finance/dashboard.html')

def update_recurring_expenses(request):
    """Update recurring expenses by creating new records for those that are due."""
    today = timezone.now().date()
    recurring_expenses = Expense.objects.filter(is_recurring=True, next_due_date__lte=today)

    for expense in recurring_expenses:
        Expense.objects.create(
            amount=expense.amount,
            category=expense.category,
            date_spent=today,
            description=expense.description,
            is_recurring=False
        )
        expense.next_due_date = expense.calculate_next_due_date()
        expense.save()

    return JsonResponse({'status': 'success'})

# AJAX CRUD operations for Expense
@require_http_methods(["GET"])
def expense_list(request):
    """Return a list of all expenses."""
    expenses = list(Expense.objects.values())
    return JsonResponse({'status': 'success', 'expenses': expenses})

@require_http_methods(["POST"])
def expense_create(request):
    """Create a new expense and return its details."""
    try:
        data = json.loads(request.body)
        required_fields = ['amount', 'category']
        for field in required_fields:
            if field not in data:
                return JsonResponse({'status': 'error', 'message': f'Missing field: {field}'}, status=400)

        expense = Expense.objects.create(
            amount=data['amount'],
            category=data['category'],
            date_spent=data.get('date_spent', timezone.now().date()),
            description=data.get('description', ''),
            is_recurring=data.get('is_recurring', False),
            recurrence_frequency=data.get('recurrence_frequency')
        )
        return JsonResponse({
            'status': 'success', 
            'expense': {
                'id': expense.id, 
                'amount': str(expense.amount),
                'category': expense.category,
                'date_spent': expense.date_spent.isoformat(),
                'description': expense.description
            }
        })
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@require_http_methods(["POST"])
def expense_update(request, expense_id):
    """Update an existing expense and return its updated details."""
    expense = get_object_or_404(Expense, id=expense_id)

    try:
        data = json.loads(request.body)
        expense.amount = data['amount']
        expense.category = data['category']
        expense.description = data.get('description', '')
        expense.date_spent = data.get('date_spent', expense.date_spent)
        expense.is_recurring = data.get('is_recurring', expense.is_recurring)
        expense.recurrence_frequency = data.get('recurrence_frequency', expense.recurrence_frequency)
        expense.save()
        return JsonResponse({'status': 'success'})
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@require_http_methods(["DELETE"])
def expense_delete(request, expense_id):
    """Delete an existing expense."""
    expense = get_object_or_404(Expense, id=expense_id)
    expense.delete()
    return JsonResponse({'status': 'success'})

# AJAX CRUD operations for Income
@require_http_methods(["GET"])
def income_list(request):
    """Return a list of all incomes."""
    incomes = list(Income.objects.values())
    return JsonResponse({'status': 'success', 'incomes': incomes})

@require_http_methods(["POST"])
def income_create(request):
    """Create a new income and return its details."""
    try:
        data = json.loads(request.body)
        required_fields = ['amount', 'source']
        for field in required_fields:
            if field not in data:
                return JsonResponse({'status': 'error', 'message': f'Missing field: {field}'}, status=400)

        income = Income.objects.create(
            amount=data['amount'],
            source=data['source'],
            date_received=data.get('date_received', timezone.now().date()),
            description=data.get('description', '')
        )
        return JsonResponse({
            'status': 'success', 
            'income': {
                'id': income.id, 
                'amount': str(income.amount),
                'source': income.source,
                'date_received': income.date_received.isoformat(),
                'description': income.description
            }
        })
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@require_http_methods(["POST"])
def income_update(request, income_id):
    """Update an existing income and return its updated details."""
    income = get_object_or_404(Income, id=income_id)

    try:
        income.amount = request.POST['amount']
        income.source = request.POST['source']
        income.description = request.POST.get('description', '')
        income.date_received = request.POST.get('date_received', income.date_received)
        income.save()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@require_http_methods(["DELETE"])
def income_delete(request, income_id):
    """Delete an existing income."""
    income = get_object_or_404(Income, id=income_id)
    income.delete()
    return JsonResponse({'status': 'success'})

# AJAX CRUD operations for Budget
@require_http_methods(["GET"])
def budget_list(request):
    """Return a list of all budgets."""
    budgets = list(Budget.objects.values())
    return JsonResponse({'status': 'success', 'budgets': budgets})

@require_http_methods(["POST"])
def budget_create(request):
    """Create a new budget and return its details."""
    try:
        data = json.loads(request.body)
        required_fields = ['category', 'limit']
        for field in required_fields:
            if field not in data:
                return JsonResponse({'status': 'error', 'message': f'Missing field: {field}'}, status=400)

        budget = Budget.objects.create(
            category=data['category'],
            limit=data['limit'],
            start_date=data.get('start_date', timezone.now().date()),
            end_date=data.get('end_date', timezone.now().date())
        )
        return JsonResponse({
            'status': 'success', 
            'budget': {
                'id': budget.id, 
                'category': budget.category,
                'limit': str(budget.limit),
                'start_date': budget.start_date.isoformat(),
                'end_date': budget.end_date.isoformat()
            }
        })
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@require_http_methods(["POST"])
def budget_update(request, budget_id):
    """Update an existing budget and return its updated details."""
    budget = get_object_or_404(Budget, id=budget_id)

    try:
        data = json.loads(request.body)
        budget.category = data['category']
        budget.limit = data['limit']
        budget.start_date = data.get('start_date', budget.start_date)
        budget.end_date = data.get('end_date', budget.end_date)
        budget.save()
        return JsonResponse({'status': 'success'})
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@require_http_methods(["DELETE"])
def budget_delete(request, budget_id):
    """Delete an existing budget."""
    budget = get_object_or_404(Budget, id=budget_id)
    budget.delete()
    return JsonResponse({'status': 'success'})

# AJAX CRUD operations for SavingsGoal
@require_http_methods(["GET"])
def savings_goal_list(request):
    """Return a list of all savings goals."""
    savings_goals = list(SavingsGoal.objects.values())
    return JsonResponse({'status': 'success', 'savings_goals': savings_goals})

@require_http_methods(["POST"])
def savings_goal_create(request):
    """Create a new savings goal and return its details."""
    try:
        data = json.loads(request.body)
        required_fields = ['goal_name', 'target_amount']
        for field in required_fields:
            if field not in data:
                return JsonResponse({'status': 'error', 'message': f'Missing field: {field}'}, status=400)

        savings_goal = SavingsGoal.objects.create(
            goal_name=data['goal_name'],
            target_amount=data['target_amount'],
            current_amount=data.get('current_amount', 0),
            target_date=data.get('target_date')
        )
        return JsonResponse({
            'status': 'success', 
            'savings_goal': {
                'id': savings_goal.id, 
                'goal_name': savings_goal.goal_name,
                'target_amount': str(savings_goal.target_amount),
                'current_amount': str(savings_goal.current_amount),
                'target_date': savings_goal.target_date.isoformat() if savings_goal.target_date else None
            }
        })
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@require_http_methods(["POST"])
def savings_goal_update(request, savings_goal_id):
    """Update an existing savings goal and return its updated details."""
    savings_goal = get_object_or_404(SavingsGoal, id=savings_goal_id)

    try:
        data = json.loads(request.body)
        savings_goal.goal_name = data['goal_name']
        savings_goal.target_amount = data['target_amount']
        savings_goal.current_amount = data.get('current_amount', savings_goal.current_amount)
        savings_goal.target_date = data.get('target_date', savings_goal.target_date)
        savings_goal.save()
        return JsonResponse({'status': 'success'})
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@require_http_methods(["DELETE"])
def savings_goal_delete(request, savings_goal_id):
    """Delete an existing savings goal."""
    savings_goal = get_object_or_404(SavingsGoal, id=savings_goal_id)
    savings_goal.delete()
    return JsonResponse({'status': 'success'})

# Chart data functions
@require_http_methods(["GET"])
def expense_chart_data(request):
    """Return aggregated expense data for charting."""
    expenses = Expense.objects.annotate(month=TruncMonth('date_spent')).values('month').annotate(total=Sum('amount')).order_by('month')
    chart_data = {expense['month'].strftime('%Y-%m'): expense['total'] for expense in expenses}
    return JsonResponse({'status': 'success', 'chart_data': chart_data})

@require_http_methods(["GET"])
def income_chart_data(request):
    """Return aggregated income data for charting."""
    incomes = Income.objects.annotate(month=TruncMonth('date_received')).values('month').annotate(total=Sum('amount')).order_by('month')
    chart_data = {income['month'].strftime('%Y-%m'): income['total'] for income in incomes}
    return JsonResponse({'status': 'success', 'chart_data': chart_data})

@require_http_methods(["GET"])
def budget_chart_data(request):
    """Return aggregated budget data for charting."""
    budgets = Budget.objects.values('category').annotate(total=Sum('limit'))
    chart_data = {budget['category']: budget['total'] for budget in budgets}
    return JsonResponse({'status': 'success', 'chart_data': chart_data})


