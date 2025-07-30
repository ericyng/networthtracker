from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Main dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Account URLs
    path('accounts/', views.accounts_list, name='accounts_list'),
    path('accounts/create/', views.account_create, name='account_create'),
    path('accounts/<int:account_id>/', views.account_detail, name='account_detail'),
    path('accounts/<int:account_id>/edit/', views.account_edit, name='account_edit'),
    path('accounts/<int:account_id>/delete/', views.account_delete, name='account_delete'),
    
    # Account Entries URLs
    path('entries/', views.account_entries, name='account_entries'),
    
    # Transaction URLs
    path('transactions/', views.transactions_list, name='transactions_list'),
    path('transactions/create/', views.transaction_create, name='transaction_create'),
    path('transactions/<int:transaction_id>/edit/', views.transaction_edit, name='transaction_edit'),
    path('transactions/<int:transaction_id>/delete/', views.transaction_delete, name='transaction_delete'),
    
    # Settings URLs
    path('settings/', views.settings, name='settings'),
    path('data-management/', views.data_management, name='data_management'),
    
    # Export URLs
    path('export/csv/<str:data_type>/', views.export_csv, name='export_csv'),
    path('export/excel/<str:data_type>/', views.export_excel, name='export_excel'),
    path('export/pdf/<str:data_type>/', views.export_pdf, name='export_pdf'),
    
    # Support URL
    path('support/', views.support, name='support'),
    
    # Legal URLs
    path('terms/', views.terms_of_service, name='terms_of_service'),
    path('privacy/', views.privacy_policy, name='privacy_policy'),
] 