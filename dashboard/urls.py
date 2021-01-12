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
    path('upload_invoice/', views.upload_invoice, name='upload_invoice'),
    path('upload_credit_note/', views.upload_credit_note, name='upload_credit_note'),
    path('update_urainvoicenum_qrcode/', views.update_urainvoicenum_qrcode, name='update_urainvoicenum_qrcode'),
    path('update_credit_note_header/', views.update_credit_note_header, name='update_credit_note_header'),
    path('search_invoice/', views.search_invoice, name='search_invoice'),
    path('search_credit_note/', views.search_credit_note, name='search_credit_note'),
    path('update_credit_note_id/', views.update_credit_note_id, name='update_credit_note_id'),
    path('update_credit_note_three/', views.update_credit_note_three, name='update_credit_note_three'),
    path('dd/', views.dd, name='dd'),
]