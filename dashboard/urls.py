from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='dashboard/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('credit_notes/', views.credit_notes, name='credit_notes'),
    path('invoices/', views.invoices, name='invoices'),
    path('load_credit_notes/', views.load_credit_notes, name='load_credit_notes'),
    path('load_invoices/', views.load_invoices, name='load_invoices'),
    path('load_company_info/', views.load_company_info, name='load_company_info'),
    path('upload_document/', views.upload_document, name='upload_document'),
    path('update_external_document_number/', views.update_external_document_number, name='update_external_document_number'),
]