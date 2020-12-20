from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('items/', views.items, name='items'),
    path('invoices/', views.invoices, name='invoices'),
    path('load_items/', views.load_items, name='load_items'),
    path('load_invoices/', views.load_invoices, name='load_invoices'),
    path('load_company_info/', views.load_company_info, name='load_company_info'),
    path('upload_document/', views.upload_document, name='upload_document'),
]