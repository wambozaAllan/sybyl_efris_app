from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

import requests

def items(request):
    context = {
        'page': 'Items',
    }
    return render(request, 'dashboard/items.html', context)

def invoices(request):
    context = {
        'page': 'Invoices',
    }
    return render(request, 'dashboard/invoices.html', context)

def login(request):
    context = {
        'page': 'Login',
    }
    return render(request, 'dashboard/login.html', context)

def load_items(request):
    url = 'http://localhost:8280/services/GetItems/getitems'
    response = requests.get(url, headers={'Accept':'application/json'})
    data = {}
    if response.status_code == 200:
        print(response.headers.get('Content-Type'))
        data = response.json()
        return JsonResponse(data, status=200)
    
    else: 
        return JsonResponse(data, status=400)

def load_invoices(request):
    url = 'http://localhost:8280/services/GetOrders/getorders'
    response = requests.get(url, headers={'Accept':'application/json'})
    data = {}
    if response.status_code == 200:
        print(response.headers.get('Content-Type'))
        data = response.json()
        return JsonResponse(data, status=200)
    
    else: 
        return JsonResponse(data, status=400)


def load_company_info(request):
    url = 'http://localhost:8280/services/GetCompanyInformation/getcompanyinfor'
    response = requests.get(url, headers={'Accept':'application/json'})
    data = {}
    if response.status_code == 200:
        print(response.headers.get('Content-Type'))
        data = response.json()
        return JsonResponse(data, status=200)
    
    else: 
        return JsonResponse(data, status=400)