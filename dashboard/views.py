from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Sum, Q, Count, Avg
from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
import json
from decimal import Decimal
from .models import Account, Transaction, AccountEntry


def landing_page(request):
    """Landing page view for non-authenticated users"""
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')
    return render(request, 'dashboard/landing.html')


def signup_disabled(request):
    """View for when sign-ups are disabled"""
    return render(request, 'dashboard/signup_disabled.html')


@login_required
def dashboard(request):
    """Main dashboard view"""
    user = request.user
    
    # Get user's accounts
    accounts = Account.objects.filter(user=user, is_active=True)
    
    # Calculate current net worth
    total_assets = 0
    total_liabilities = 0
    
    for account in accounts:
        balance = account.get_latest_balance()
        if account.account_type in ['loan', 'credit']:
            total_liabilities += abs(balance)
        else:
            total_assets += balance
    
    net_worth = total_assets - total_liabilities
    
    # Get recent transactions
    recent_transactions = Transaction.objects.filter(user=user).order_by('-date')[:10]
    
    # Get account balances for chart
    account_balances = []
    for account in accounts:
        balance = account.get_latest_balance()
        if balance != 0:
            account_balances.append({
                'name': account.name,
                'balance': float(balance),
                'type': account.account_type,
                'color': get_account_color(account.account_type)
            })
    
    context = {
        'net_worth': net_worth,
        'total_assets': total_assets,
        'total_liabilities': total_liabilities,
        'accounts': accounts,
        'recent_transactions': recent_transactions,
        'account_balances': json.dumps(account_balances),
    }
    
    return render(request, 'dashboard/dashboard.html', context)


@login_required
def analytics(request):
    """Analytics page with detailed financial insights"""
    user = request.user
    
    # Get date range (last 12 months by default)
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=365)
    
    # Get user's accounts
    accounts = Account.objects.filter(user=user, is_active=True)
    
    # Net Worth Trends (last 12 months)
    net_worth_data = get_net_worth_trends(user, start_date, end_date)
    
    # Asset Allocation
    asset_allocation = get_asset_allocation(user)
    
    # Income vs Expenses (last 6 months)
    income_expenses = get_income_expenses(user, 6)
    
    # Spending by Category
    spending_by_category = get_spending_by_category(user, 6)
    
    # Account Performance
    account_performance = get_account_performance(user)
    
    # Monthly Savings Rate
    savings_rate = get_savings_rate(user, 6)
    
    # Financial Ratios
    financial_ratios = get_financial_ratios(user)
    
    # Recent Activity
    recent_activity = get_recent_activity(user)
    
    context = {
        'net_worth_data': json.dumps(net_worth_data),
        'asset_allocation': json.dumps(asset_allocation),
        'income_expenses': json.dumps(income_expenses),
        'spending_by_category': json.dumps(spending_by_category),
        'account_performance': json.dumps(account_performance),
        'savings_rate': json.dumps(savings_rate),
        'financial_ratios': financial_ratios,
        'recent_activity': recent_activity,
        'accounts': accounts,
    }
    
    return render(request, 'dashboard/analytics.html', context)


def get_net_worth_trends(user, start_date, end_date):
    """Get net worth trends over time"""
    trends = []
    current_date = start_date
    
    while current_date <= end_date:
        month = current_date.month
        year = current_date.year
        
        # Calculate net worth for this month
        accounts = Account.objects.filter(user=user, is_active=True)
        total_assets = 0
        total_liabilities = 0
        
        for account in accounts:
            balance = account.get_latest_balance(month, year)
            if account.account_type in ['loan', 'credit']:
                total_liabilities += abs(balance)
            else:
                total_assets += balance
        
        net_worth = total_assets - total_liabilities
        
        trends.append({
            'date': current_date.strftime('%Y-%m'),
            'net_worth': float(net_worth),
            'assets': float(total_assets),
            'liabilities': float(total_liabilities)
        })
        
        # Move to next month
        if current_date.month == 12:
            current_date = current_date.replace(year=current_date.year + 1, month=1)
        else:
            current_date = current_date.replace(month=current_date.month + 1)
    
    return trends


def get_asset_allocation(user):
    """Get asset allocation breakdown"""
    accounts = Account.objects.filter(user=user, is_active=True)
    allocation = {}
    
    for account in accounts:
        balance = account.get_latest_balance()
        if balance > 0 and account.account_type not in ['loan', 'credit']:
            asset_type = account.asset_type
            if asset_type not in allocation:
                allocation[asset_type] = 0
            allocation[asset_type] += float(balance)
    
    # Convert to chart format
    chart_data = []
    colors = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40']
    
    for i, (asset_type, amount) in enumerate(allocation.items()):
        chart_data.append({
            'label': asset_type.replace('_', ' ').title(),
            'value': amount,
            'color': colors[i % len(colors)]
        })
    
    return chart_data


def get_income_expenses(user, months=6):
    """Get income vs expenses over time"""
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=months * 30)
    
    transactions = Transaction.objects.filter(
        user=user,
        date__gte=start_date,
        date__lte=end_date
    )
    
    monthly_data = {}
    
    for transaction in transactions:
        month_key = transaction.date.strftime('%Y-%m')
        if month_key not in monthly_data:
            monthly_data[month_key] = {'income': 0, 'expenses': 0}
        
        if transaction.transaction_type == 'income':
            monthly_data[month_key]['income'] += float(transaction.amount)
        elif transaction.transaction_type == 'expense':
            monthly_data[month_key]['expenses'] += float(transaction.amount)
    
    # Convert to chart format
    chart_data = {
        'labels': list(monthly_data.keys()),
        'income': [monthly_data[month]['income'] for month in monthly_data.keys()],
        'expenses': [monthly_data[month]['expenses'] for month in monthly_data.keys()]
    }
    
    return chart_data


def get_spending_by_category(user, months=6):
    """Get spending breakdown by category"""
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=months * 30)
    
    transactions = Transaction.objects.filter(
        user=user,
        transaction_type='expense',
        date__gte=start_date,
        date__lte=end_date
    ).values('category').annotate(total=Sum('amount'))
    
    chart_data = []
    colors = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40', '#FF6384', '#36A2EB']
    
    for i, item in enumerate(transactions):
        chart_data.append({
            'label': item['category'].replace('_', ' ').title(),
            'value': float(item['total']),
            'color': colors[i % len(colors)]
        })
    
    return chart_data


def get_account_performance(user):
    """Get account performance over time"""
    accounts = Account.objects.filter(user=user, is_active=True)
    performance_data = []
    
    for account in accounts:
        # Get last 6 months of data
        entries = account.entries.order_by('-year', '-month')[:6]
        
        if entries:
            balances = [float(entry.balance) for entry in entries]
            performance_data.append({
                'account_name': account.name,
                'account_type': account.account_type,
                'balances': balances,
                'growth_rate': calculate_growth_rate(balances) if len(balances) > 1 else 0
            })
    
    return performance_data


def get_savings_rate(user, months=6):
    """Calculate monthly savings rate"""
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=months * 30)
    
    transactions = Transaction.objects.filter(
        user=user,
        date__gte=start_date,
        date__lte=end_date
    )
    
    total_income = sum(float(t.amount) for t in transactions if t.transaction_type == 'income')
    total_expenses = sum(float(t.amount) for t in transactions if t.transaction_type == 'expense')
    
    if total_income > 0:
        savings_rate = ((total_income - total_expenses) / total_income) * 100
    else:
        savings_rate = 0
    
    return {
        'savings_rate': round(savings_rate, 2),
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_savings': total_income - total_expenses
    }


def get_financial_ratios(user):
    """Calculate key financial ratios"""
    accounts = Account.objects.filter(user=user, is_active=True)
    
    total_assets = 0
    total_liabilities = 0
    liquid_assets = 0
    monthly_expenses = 0
    
    for account in accounts:
        balance = account.get_latest_balance()
        if account.account_type in ['loan', 'credit']:
            total_liabilities += abs(balance)
        else:
            total_assets += balance
            if account.account_type in ['checking', 'savings']:
                liquid_assets += balance
    
    # Calculate monthly expenses (last 3 months average)
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=90)
    
    recent_expenses = Transaction.objects.filter(
        user=user,
        transaction_type='expense',
        date__gte=start_date,
        date__lte=end_date
    )
    
    if recent_expenses:
        monthly_expenses = float(recent_expenses.aggregate(Sum('amount'))['amount__sum'] or 0) / 3
    
    ratios = {
        'debt_to_income': (total_liabilities / total_assets * 100) if total_assets > 0 else 0,
        'emergency_fund_ratio': (liquid_assets / monthly_expenses) if monthly_expenses > 0 else 0,
        'net_worth': total_assets - total_liabilities,
        'asset_diversity': len(set(account.asset_type for account in accounts if account.get_latest_balance() > 0))
    }
    
    return ratios


def get_recent_activity(user):
    """Get recent financial activity"""
    recent_transactions = Transaction.objects.filter(user=user).order_by('-date')[:20]
    recent_entries = AccountEntry.objects.filter(account__user=user).order_by('-created_at')[:10]
    
    return {
        'transactions': recent_transactions,
        'entries': recent_entries
    }


def calculate_growth_rate(balances):
    """Calculate growth rate from balance history"""
    if len(balances) < 2:
        return 0
    
    initial = balances[-1]
    final = balances[0]
    
    if initial == 0:
        return 0
    
    return ((final - initial) / initial) * 100


def get_account_color(account_type):
    """Get color for account type"""
    colors = {
        'checking': '#36A2EB',
        'savings': '#4BC0C0',
        'investment': '#FFCE56',
        'credit': '#FF6384',
        'loan': '#9966FF',
        'other': '#FF9F40'
    }
    return colors.get(account_type, '#FF9F40')


@login_required
def accounts_list(request):
    """List all user accounts"""
    accounts = Account.objects.filter(user=request.user, is_active=True)
    return render(request, 'dashboard/accounts_list.html', {'accounts': accounts})


@login_required
def account_detail(request, account_id):
    """Show account details"""
    account = get_object_or_404(Account, id=account_id, user=request.user)
    entries = account.entries.order_by('-year', '-month')
    transactions = account.transactions.order_by('-date')
    
    context = {
        'account': account,
        'entries': entries,
        'transactions': transactions
    }
    return render(request, 'dashboard/account_detail.html', context)


@login_required
def transactions_list(request):
    """List all user transactions"""
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'dashboard/transactions_list.html', {'transactions': transactions})


@login_required
def settings(request):
    """User settings page"""
    return render(request, 'dashboard/settings.html')


def terms_of_service(request):
    """Terms of service page"""
    return render(request, 'dashboard/terms_of_service.html')


def privacy_policy(request):
    """Privacy policy page"""
    return render(request, 'dashboard/privacy_policy.html')
