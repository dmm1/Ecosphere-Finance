from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    
    # Income URLs
    path('incomes/', views.income_list, name='income_list'),
    path('incomes/create/', views.income_create, name='income_create'),
    path('incomes/<int:pk>/update/', views.income_update, name='income_update'),
    path('incomes/<int:pk>/delete/', views.income_delete, name='income_delete'),

    # Expense URLs
    path('expenses/', views.expense_list, name='expense_list'),
    path('expenses/create/', views.expense_create, name='expense_create'),
    path('expenses/<int:pk>/update/', views.expense_update, name='expense_update'),
    path('expenses/<int:pk>/delete/', views.expense_delete, name='expense_delete'),

    # Budget URLs
    path('budgets/', views.budget_list, name='budget_list'),
    path('budgets/create/', views.budget_create, name='budget_create'),
    path('budgets/<int:pk>/update/', views.budget_update, name='budget_update'),
    path('budgets/<int:pk>/delete/', views.budget_delete, name='budget_delete'),

    # Savings Goal URLs
    path('savings_goals/', views.savings_goal_list, name='savings_goal_list'),
    path('savings_goals/create/', views.savings_goal_create, name='savings_goal_create'),
    path('savings_goals/<int:pk>/update/', views.savings_goal_update, name='savings_goal_update'),
    path('savings_goals/<int:pk>/delete/', views.savings_goal_delete, name='savings_goal_delete'),

    # Chart data URLs for statistics
    path('chart_data/expenses/', views.expense_chart_data, name='expense_chart_data'),
    path('chart_data/incomes/', views.income_chart_data, name='income_chart_data'),
    path('chart_data/budgets/', views.budget_chart_data, name='budget_chart_data'),
]
