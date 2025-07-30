from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum, Q
from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .models import Account, Transaction, AccountEntry
from .forms import AccountForm, TransactionForm, AccountEntryForm


@login_required
def dashboard(request):
    """Main dashboard view showing overview of accounts"""
    user = request.user
    
    # Get user's accounts
    accounts = Account.objects.filter(user=user, is_active=True)
    
    # Calculate total balance across all accounts using latest entries
    total_balance = sum(account.get_latest_balance() for account in accounts)
    
    # Get time series data for the bar chart (last 12 months)
    from django.db.models import Sum
    from datetime import datetime, timedelta
    
    # Get the current month and year
    current_date = timezone.now()
    chart_data = []
    
    # Generate data for the last 12 months
    for i in range(11, -1, -1):  # 11 to 0 (last 12 months)
        target_date = current_date - timedelta(days=30*i)
        month = target_date.month
        year = target_date.year
        
        # Get total balance for this month/year
        monthly_balance = AccountEntry.objects.filter(
            account__user=user,
            month=month,
            year=year
        ).aggregate(total=Sum('balance'))['total'] or 0
        
        chart_data.append({
            'month': target_date.strftime('%b %Y'),
            'balance': float(monthly_balance),
            'month_num': month,
            'year': year
        })
    
    context = {
        'accounts': accounts,
        'total_balance': total_balance,
        'has_accounts': accounts.exists(),
        'chart_data': chart_data,
    }
    
    return render(request, 'dashboard/dashboard.html', context)


@login_required
def accounts_list(request):
    """View to list all user accounts"""
    accounts = Account.objects.filter(user=request.user, is_active=True)
    
    # Get sorting parameters
    sort_by = request.GET.get('sort', 'name')
    order = request.GET.get('order', 'asc')
    
    # Validate sort field
    valid_sort_fields = ['name', 'account_type', 'classification', 'asset_type', 'institution', 'balance']
    if sort_by not in valid_sort_fields:
        sort_by = 'name'
    
    # Apply sorting
    if sort_by == 'balance':
        # For balance sorting, we need to annotate with the latest balance
        accounts = accounts.annotate(
            latest_balance=models.Subquery(
                AccountEntry.objects.filter(
                    account=models.OuterRef('pk')
                ).order_by('-year', '-month').values('balance')[:1]
            )
        )
        if order == 'desc':
            accounts = accounts.order_by('-latest_balance')
        else:
            accounts = accounts.order_by('latest_balance')
    else:
        if order == 'desc':
            accounts = accounts.order_by(f'-{sort_by}')
        else:
            accounts = accounts.order_by(sort_by)
    
    # Calculate summary statistics using latest entries
    total_balance = sum(account.get_latest_balance() for account in accounts)
    
    # Group accounts by classification
    accounts_by_classification = {}
    for account in accounts:
        classification = account.get_classification_display()
        if classification not in accounts_by_classification:
            accounts_by_classification[classification] = []
        accounts_by_classification[classification].append(account)
    
    context = {
        'accounts': accounts,
        'accounts_by_classification': accounts_by_classification,
        'total_balance': total_balance,
        'sort_by': sort_by,
        'order': order,
    }
    return render(request, 'dashboard/accounts_list.html', context)


@login_required
def account_detail(request, account_id):
    """View to show account details and transactions"""
    account = get_object_or_404(Account, id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date', '-created_at')
    
    context = {
        'account': account,
        'transactions': transactions,
    }
    return render(request, 'dashboard/account_detail.html', context)


@login_required
def account_create(request):
    """View to create a new account"""
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard:accounts_list')
    else:
        form = AccountForm()
    
    return render(request, 'dashboard/account_form.html', {'form': form, 'title': 'Add New Account'})


@login_required
def account_edit(request, account_id):
    """View to edit an existing account"""
    account = get_object_or_404(Account, id=account_id, user=request.user)
    
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account updated successfully!')
            return redirect('dashboard:accounts_list')
    else:
        form = AccountForm(instance=account)
    
    return render(request, 'dashboard/account_form.html', {
        'form': form, 
        'title': 'Edit Account',
        'account': account
    })


@login_required
def account_delete(request, account_id):
    """View to delete an account"""
    account = get_object_or_404(Account, id=account_id, user=request.user)
    
    if request.method == 'POST':
        account.is_active = False
        account.save()
        messages.success(request, 'Account deleted successfully!')
        return redirect('dashboard:accounts_list')
    
    return render(request, 'dashboard/account_confirm_delete.html', {'account': account})


@login_required
def transactions_list(request):
    """View to list all transactions"""
    transactions = Transaction.objects.filter(user=request.user).order_by('-date', '-created_at')
    
    # Filter options
    account_filter = request.GET.get('account')
    category_filter = request.GET.get('category')
    transaction_type_filter = request.GET.get('transaction_type')
    
    if account_filter:
        transactions = transactions.filter(account_id=account_filter)
    if category_filter:
        transactions = transactions.filter(category=category_filter)
    if transaction_type_filter:
        transactions = transactions.filter(transaction_type=transaction_type_filter)
    
    accounts = Account.objects.filter(user=request.user, is_active=True)
    
    # Calculate summary statistics
    total_income = transactions.filter(transaction_type='income').aggregate(total=Sum('amount'))['total'] or 0
    total_expenses = transactions.filter(transaction_type='expense').aggregate(total=Sum('amount'))['total'] or 0
    
    context = {
        'transactions': transactions,
        'accounts': accounts,
        'categories': Transaction.CATEGORIES,
        'transaction_types': Transaction.TRANSACTION_TYPES,
        'account_filter': account_filter,
        'category_filter': category_filter,
        'transaction_type_filter': transaction_type_filter,
        'total_income': total_income,
        'total_expenses': total_expenses,
    }
    return render(request, 'dashboard/transactions_list.html', context)


@login_required
def transaction_create(request):
    """View to create a new transaction"""
    if request.method == 'POST':
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, 'Transaction added successfully!')
            return redirect('dashboard:transactions_list')
    else:
        form = TransactionForm(user=request.user)
    
    return render(request, 'dashboard/transaction_form.html', {
        'form': form, 
        'title': 'Add New Transaction'
    })


@login_required
def transaction_edit(request, transaction_id):
    """View to edit an existing transaction"""
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)
    
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transaction updated successfully!')
            return redirect('dashboard:transactions_list')
    else:
        form = TransactionForm(instance=transaction, user=request.user)
    
    return render(request, 'dashboard/transaction_form.html', {
        'form': form, 
        'title': 'Edit Transaction',
        'transaction': transaction
    })


@login_required
def transaction_delete(request, transaction_id):
    """View to delete a transaction"""
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)
    
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'Transaction deleted successfully!')
        return redirect('dashboard:transactions_list')
    
    return render(request, 'dashboard/transaction_confirm_delete.html', {'transaction': transaction})


@login_required
def account_entries(request):
    """View to manage account entries for current month"""
    user = request.user
    current_month = timezone.now().month
    current_year = timezone.now().year
    
    # Get selected month/year from request
    selected_month = int(request.GET.get('month', current_month))
    selected_year = int(request.GET.get('year', current_year))
    
    # Get sorting parameters
    sort_by = request.GET.get('sort', 'name')
    order = request.GET.get('order', 'asc')
    
    # Validate sort field
    valid_sort_fields = ['name', 'account_type', 'classification', 'asset_type', 'institution', 'balance']
    if sort_by not in valid_sort_fields:
        sort_by = 'name'
    
    # Get all user accounts with sorting
    accounts = Account.objects.filter(user=user, is_active=True)
    
    # Apply sorting
    if sort_by == 'balance':
        # For balance sorting, we need to annotate with the latest balance
        accounts = accounts.annotate(
            latest_balance=models.Subquery(
                AccountEntry.objects.filter(
                    account=models.OuterRef('pk')
                ).order_by('-year', '-month').values('balance')[:1]
            )
        )
        if order == 'desc':
            accounts = accounts.order_by('-latest_balance')
        else:
            accounts = accounts.order_by('latest_balance')
    else:
        if order == 'desc':
            accounts = accounts.order_by(f'-{sort_by}')
        else:
            accounts = accounts.order_by(sort_by)
    
    if request.method == 'POST':
        # Handle form submission for multiple accounts
        success_count = 0
        for account in accounts:
            balance_key = f'balance_{account.id}'
            notes_key = f'notes_{account.id}'
            
            if balance_key in request.POST:
                balance = request.POST.get(balance_key)
                notes = request.POST.get(notes_key, '')
                
                if balance:  # Only save if balance is provided
                    entry, created = AccountEntry.objects.get_or_create(
                        account=account,
                        month=selected_month,
                        year=selected_year,
                        defaults={'balance': balance, 'notes': notes}
                    )
                    if not created:
                        entry.balance = balance
                        entry.notes = notes
                        entry.save()
                    success_count += 1
        
        if success_count > 0:
            messages.success(request, f'Successfully updated {success_count} account entries for {selected_month}/{selected_year}')
        return redirect('dashboard:account_entries')
    
    # Get existing entries for the selected month/year
    entries = {}
    for account in accounts:
        entry = AccountEntry.objects.filter(
            account=account,
            month=selected_month,
            year=selected_year
        ).first()
        
        if not entry:
            # Try to get the previous month's entry as default
            prev_entry = AccountEntry.objects.filter(
                account=account
            ).order_by('-year', '-month').first()
            
            if prev_entry:
                entry = AccountEntry(
                    account=account,
                    month=selected_month,
                    year=selected_year,
                    balance=prev_entry.balance,
                    notes=''
                )
            else:
                entry = AccountEntry(
                    account=account,
                    month=selected_month,
                    year=selected_year,
                    balance=0.00,
                    notes=''
                )
        
        entries[account.id] = entry
    
    # Group accounts by classification
    accounts_by_classification = {}
    for account in accounts:
        classification = account.get_classification_display()
        if classification not in accounts_by_classification:
            accounts_by_classification[classification] = []
        accounts_by_classification[classification].append(account)
    
    context = {
        'accounts': accounts,
        'accounts_by_classification': accounts_by_classification,
        'entries': entries,
        'selected_month': selected_month,
        'selected_year': selected_year,
        'current_month': current_month,
        'current_year': current_year,
        'sort_by': sort_by,
        'order': order,
    }
    
    return render(request, 'dashboard/account_entries.html', context)


@login_required
def settings(request):
    """View for account settings"""
    user = request.user
    
    if request.method == 'POST':
        # Handle form submission for updating user profile
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        
        # Basic validation
        if not email:
            messages.error(request, 'Email is required.')
            return redirect('dashboard:settings')
        
        # Check if email is already taken by another user
        if User.objects.filter(email=email).exclude(id=user.id).exists():
            messages.error(request, 'This email is already in use by another account.')
            return redirect('dashboard:settings')
        
        # Update user profile
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('dashboard:settings')
    
    # Get account statistics
    accounts_count = Account.objects.filter(user=user, is_active=True).count()
    transactions_count = Transaction.objects.filter(account__user=user).count()
    entries_count = AccountEntry.objects.filter(account__user=user).count()
    
    context = {
        'user': user,
        'accounts_count': accounts_count,
        'transactions_count': transactions_count,
        'entries_count': entries_count,
    }
    
    return render(request, 'dashboard/settings.html', context)


@login_required
def data_management(request):
    """View for data management options"""
    user = request.user
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'delete_accounts':
            # Delete all user's accounts and related data
            accounts = Account.objects.filter(user=user)
            accounts_count = accounts.count()
            
            # Delete related entries and transactions
            AccountEntry.objects.filter(account__user=user).delete()
            Transaction.objects.filter(account__user=user).delete()
            accounts.delete()
            
            messages.success(request, f'Successfully deleted {accounts_count} accounts and all related data.')
            return redirect('dashboard:dashboard')
            
        elif action == 'delete_transactions':
            # Delete all transactions
            transactions = Transaction.objects.filter(account__user=user)
            transactions_count = transactions.count()
            transactions.delete()
            
            messages.success(request, f'Successfully deleted {transactions_count} transactions.')
            return redirect('dashboard:data_management')
            
        elif action == 'delete_entries':
            # Delete all account entries
            entries = AccountEntry.objects.filter(account__user=user)
            entries_count = entries.count()
            entries.delete()
            
            messages.success(request, f'Successfully deleted {entries_count} account entries.')
            return redirect('dashboard:data_management')
    
    # Get data statistics
    accounts_count = Account.objects.filter(user=user, is_active=True).count()
    transactions_count = Transaction.objects.filter(account__user=user).count()
    entries_count = AccountEntry.objects.filter(account__user=user).count()
    
    context = {
        'accounts_count': accounts_count,
        'transactions_count': transactions_count,
        'entries_count': entries_count,
    }
    
    return render(request, 'dashboard/data_management.html', context)



