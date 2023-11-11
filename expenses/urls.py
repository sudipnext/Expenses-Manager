from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns =[
    path('', views.home, name="expenses"),
    path('add-expenses', views.add_expense, name="add-expenses"),
    path('edit-expense/<int:id>', views.ExpenseEdit, name="expense-edit"),
    path('delete-expense/<int:id>', views.ExpenseDelete, name="expense-delete"),
    path('search-expenses', csrf_exempt(views.searchExpenses), name="search-expenses"),


] 