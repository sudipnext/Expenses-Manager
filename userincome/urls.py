from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns =[
    path('', views.home, name="userincome"),
    path('add-income', views.add_income, name="add-income"),
    path('edit-income/<int:id>', views.UserIncomeEdit, name="income-edit"),
    path('delete-income/<int:id>', views.UserIncomeDelete, name="income-delete"),
    path('search-income', csrf_exempt(views.searchIncomes), name="search-income"),


] 