from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Source, UserIncome
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import UserPreference


def searchIncomes(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get('searchText')
        userincome = UserIncome.objects.filter(amount__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(date__icontains=search_str, owner=request.user) | UserIncome.objects.filter(description__icontains=search_str, owner=request.user) | UserIncome.objects.filter(source__icontains=search_str, owner=request.user)
        data = userincome.values()
        return JsonResponse(list(data), safe=False)


# Create your views here.
@login_required(login_url='/authentication/login')
def home(request):
    
    userincome = UserIncome.objects.filter(owner=request.user)
    paginator=Paginator(userincome, 2)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreference.objects.get(user=request.user).currency
    context ={
        'userincome':userincome,
        'page_obj':page_obj,
        'currency':currency
        
    }
    return render(request, 'userincome/index.html', context)

@login_required(login_url='/authentication/login')
def add_income(request):
    sources = Source.objects.all()
    context ={
        'sources':sources,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'userincome/add_userincome.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['date']
        source = request.POST['source']
        if not amount:
            messages.error(request, 'Amount is Required')
            return render(request, 'userincome/add_userincome.html', context)    
        if not description:
            messages.error(request, 'Description is Required')
            return render(request, 'userincome/add_userincome.html', context)
        UserIncome.objects.create(owner = request.user,amount=amount, date=date, source=source, description=description )
        messages.success(request, 'UserIncomes Saved SuccessFully!')

        return redirect('userincome')
    

def UserIncomeEdit(request, id):
    userincome = UserIncome.objects.get(pk=id)
    sources = Source.objects.all()
    context = {
        'userincome':userincome,
        'values': userincome,
        'sources':sources
    }
    if request.method == 'GET':
        return render(request, 'userincome/edit-userincome.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['date']
        source = request.POST['source']
        if not amount:
            messages.error(request, 'Amount is Required')
            return render(request, 'userincome/edit-userincome.html', context)    
        if not description:
            messages.error(request, 'Description is Required')
            return render(request, 'userincome/edit-userincome.html', context)
        userincome.owner=request.user
        userincome.amount=amount
        userincome.date=date
        userincome.source = source
        userincome.description = description
        userincome.save()
        messages.success(request, 'UserIncomes Updated SuccessFully!')

        return redirect('userincome')


def UserIncomeDelete(request, id):
    userincome = UserIncome.objects.get(pk=id)
    userincome.delete()
    messages.success(request, 'UserIncome Deleted Sucessfully')
    return redirect('userincome')


    



