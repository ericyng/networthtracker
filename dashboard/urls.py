from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Landing page
    path('landing/', views.landing_page, name='landing'),
    
    # Main dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Analytics page
    path('analytics/', views.analytics, name='analytics'),
    
    # Account URLs
    path('accounts/', views.accounts_list, name='accounts_list'),
    path('accounts/<int:account_id>/', views.account_detail, name='account_detail'),
    
    # Transaction URLs
    path('transactions/', views.transactions_list, name='transactions_list'),
    
    # Settings URLs
    path('settings/', views.settings, name='settings'),
    
    # Legal URLs
    path('terms/', views.terms_of_service, name='terms_of_service'),
    path('privacy/', views.privacy_policy, name='privacy_policy'),
    
    # Signup disabled
    path('signup-disabled/', views.signup_disabled, name='signup_disabled'),
]
