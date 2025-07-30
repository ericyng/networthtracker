from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from decimal import Decimal
from datetime import date, timedelta
import json

from .models import Account, Transaction, AccountEntry
from .forms import AccountForm, TransactionForm, AccountEntryForm


class AccountModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_account_creation(self):
        """Test creating an account"""
        account = Account.objects.create(
            user=self.user,
            name='Test Checking Account',
            account_type='checking',
            classification='taxable',
            asset_type='cash',
            currency='USD',
            institution='Test Bank',
            account_number='123456789'
        )
        
        self.assertEqual(account.name, 'Test Checking Account')
        self.assertEqual(account.account_type, 'checking')
        self.assertEqual(account.classification, 'taxable')
        self.assertEqual(account.asset_type, 'cash')
        self.assertEqual(account.currency, 'USD')
        self.assertEqual(account.institution, 'Test Bank')
        self.assertEqual(account.account_number, '123456789')
        self.assertTrue(account.is_active)
        self.assertEqual(account.user, self.user)
        
    def test_account_str_representation(self):
        """Test account string representation"""
        account = Account.objects.create(
            user=self.user,
            name='Test Account',
            account_type='savings'
        )
        expected_str = f"Test Account (savings) - {self.user.username}"
        self.assertEqual(str(account), expected_str)
        
    def test_get_latest_balance_no_entries(self):
        """Test getting latest balance when no entries exist"""
        account = Account.objects.create(
            user=self.user,
            name='Test Account',
            account_type='checking'
        )
        balance = account.get_latest_balance()
        self.assertEqual(balance, 0.00)
        
    def test_get_latest_balance_with_entries(self):
        """Test getting latest balance with entries"""
        account = Account.objects.create(
            user=self.user,
            name='Test Account',
            account_type='checking'
        )
        
        # Create entries for different months
        AccountEntry.objects.create(
            account=account,
            month=1,
            year=2024,
            balance=Decimal('1000.00')
        )
        
        AccountEntry.objects.create(
            account=account,
            month=2,
            year=2024,
            balance=Decimal('1500.00')
        )
        
        # Should return the latest entry (month 2)
        balance = account.get_latest_balance()
        self.assertEqual(balance, Decimal('1500.00'))
        
    def test_get_latest_balance_specific_month(self):
        """Test getting balance for specific month"""
        account = Account.objects.create(
            user=self.user,
            name='Test Account',
            account_type='checking'
        )
        
        AccountEntry.objects.create(
            account=account,
            month=1,
            year=2024,
            balance=Decimal('1000.00')
        )
        
        AccountEntry.objects.create(
            account=account,
            month=2,
            year=2024,
            balance=Decimal('1500.00')
        )
        
        # Should return balance for month 1
        balance = account.get_latest_balance(month=1, year=2024)
        self.assertEqual(balance, Decimal('1000.00'))
        
    def test_529_classification(self):
        """Test creating an account with 529 classification"""
        account = Account.objects.create(
            user=self.user,
            name='College Savings 529',
            account_type='investment',
            classification='529',
            asset_type='cash',
            currency='USD',
            institution='Vanguard',
            account_number='529123456'
        )
        
        self.assertEqual(account.name, 'College Savings 529')
        self.assertEqual(account.account_type, 'investment')
        self.assertEqual(account.classification, '529')
        self.assertEqual(account.asset_type, 'cash')
        self.assertEqual(account.currency, 'USD')
        self.assertEqual(account.institution, 'Vanguard')
        self.assertEqual(account.account_number, '529123456')
        self.assertTrue(account.is_active)
        self.assertEqual(account.user, self.user)


class TransactionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.account = Account.objects.create(
            user=self.user,
            name='Test Account',
            account_type='checking'
        )
        
    def test_transaction_creation(self):
        """Test creating a transaction"""
        transaction = Transaction.objects.create(
            user=self.user,
            account=self.account,
            amount=Decimal('100.50'),
            transaction_type='expense',
            category='food',
            description='Grocery shopping',
            date=date(2024, 1, 15)
        )
        
        self.assertEqual(transaction.amount, Decimal('100.50'))
        self.assertEqual(transaction.transaction_type, 'expense')
        self.assertEqual(transaction.category, 'food')
        self.assertEqual(transaction.description, 'Grocery shopping')
        self.assertEqual(transaction.date, date(2024, 1, 15))
        self.assertEqual(transaction.user, self.user)
        self.assertEqual(transaction.account, self.account)
        
    def test_transaction_str_representation(self):
        """Test transaction string representation"""
        transaction = Transaction.objects.create(
            user=self.user,
            account=self.account,
            amount=Decimal('100.50'),
            transaction_type='expense',
            category='food',
            description='Grocery shopping',
            date=date(2024, 1, 15)
        )
        expected_str = "Grocery shopping - 100.50 (expense)"
        self.assertEqual(str(transaction), expected_str)


class AccountEntryModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.account = Account.objects.create(
            user=self.user,
            name='Test Account',
            account_type='checking'
        )
        
    def test_account_entry_creation(self):
        """Test creating an account entry"""
        entry = AccountEntry.objects.create(
            account=self.account,
            month=1,
            year=2024,
            balance=Decimal('5000.00'),
            notes='Monthly balance update'
        )
        
        self.assertEqual(entry.account, self.account)
        self.assertEqual(entry.month, 1)
        self.assertEqual(entry.year, 2024)
        self.assertEqual(entry.balance, Decimal('5000.00'))
        self.assertEqual(entry.notes, 'Monthly balance update')
        
    def test_account_entry_str_representation(self):
        """Test account entry string representation"""
        entry = AccountEntry.objects.create(
            account=self.account,
            month=1,
            year=2024,
            balance=Decimal('5000.00')
        )
        expected_str = f"{self.account.name} - 1/2024: $5000.00"
        self.assertEqual(str(entry), expected_str)
        
    def test_account_entry_unique_constraint(self):
        """Test that only one entry per account per month/year is allowed"""
        # Create first entry
        AccountEntry.objects.create(
            account=self.account,
            month=1,
            year=2024,
            balance=Decimal('5000.00')
        )
        
        # Try to create another entry for the same month/year
        with self.assertRaises(Exception):
            AccountEntry.objects.create(
                account=self.account,
                month=1,
                year=2024,
                balance=Decimal('6000.00')
            )


class AccountFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_account_form_valid(self):
        """Test account form with valid data"""
        form_data = {
            'name': 'Test Account',
            'account_type': 'checking',
            'classification': 'taxable',
            'asset_type': 'cash',
            'currency': 'USD',
            'institution': 'Test Bank',
            'account_number': '123456789'
        }
        form = AccountForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_account_form_invalid(self):
        """Test account form with invalid data"""
        form_data = {
            'name': '',  # Required field
            'account_type': 'invalid_type',  # Invalid choice
            'classification': 'taxable',
            'asset_type': 'cash',
            'currency': 'USD'
        }
        form = AccountForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('account_type', form.errors)


class TransactionFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.account = Account.objects.create(
            user=self.user,
            name='Test Account',
            account_type='checking'
        )
        
    def test_transaction_form_valid(self):
        """Test transaction form with valid data"""
        form_data = {
            'account': self.account.id,
            'amount': '100.50',
            'transaction_type': 'expense',
            'category': 'food',
            'description': 'Grocery shopping',
            'date': '2024-01-15'
        }
        form = TransactionForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())
        
    def test_transaction_form_invalid(self):
        """Test transaction form with invalid data"""
        form_data = {
            'account': self.account.id,
            'amount': 'invalid_amount',  # Invalid decimal
            'transaction_type': 'invalid_type',  # Invalid choice
            'category': 'food',
            'description': '',  # Required field
            'date': '2024-01-15'
        }
        form = TransactionForm(data=form_data, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('amount', form.errors)
        self.assertIn('transaction_type', form.errors)
        self.assertIn('description', form.errors)
        
    def test_transaction_form_account_queryset(self):
        """Test that form only shows user's accounts"""
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        other_account = Account.objects.create(
            user=other_user,
            name='Other Account',
            account_type='checking'
        )
        
        form = TransactionForm(user=self.user)
        self.assertIn(self.account, form.fields['account'].queryset)
        self.assertNotIn(other_account, form.fields['account'].queryset)


class AccountEntryFormTest(TestCase):
    def test_account_entry_form_valid(self):
        """Test account entry form with valid data"""
        form_data = {
            'month': 1,
            'year': 2024,
            'balance': '5000.00',
            'notes': 'Monthly balance update'
        }
        form = AccountEntryForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_account_entry_form_invalid(self):
        """Test account entry form with invalid data"""
        form_data = {
            'month': 13,  # Invalid month
            'year': 2024,
            'balance': 'invalid_balance',  # Invalid decimal
            'notes': 'Monthly balance update'
        }
        form = AccountEntryForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('month', form.errors)
        self.assertIn('balance', form.errors)


class DashboardViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.account = Account.objects.create(
            user=self.user,
            name='Test Account',
            account_type='checking',
            classification='taxable',
            asset_type='cash'
        )
        
    def test_dashboard_view_authenticated(self):
        """Test dashboard view for authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/dashboard.html')
        
    def test_dashboard_view_unauthenticated(self):
        """Test dashboard view redirects unauthenticated users"""
        response = self.client.get(reverse('dashboard:dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
    def test_dashboard_with_account_entries(self):
        """Test dashboard with account entries"""
        self.client.login(username='testuser', password='testpass123')
        
        # Create account entry
        AccountEntry.objects.create(
            account=self.account,
            month=timezone.now().month,
            year=timezone.now().year,
            balance=Decimal('5000.00')
        )
        
        response = self.client.get(reverse('dashboard:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('total_balance', response.context)
        self.assertEqual(response.context['total_balance'], Decimal('5000.00'))
        
    def test_accounts_list_view(self):
        """Test accounts list view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard:accounts_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/accounts_list.html')
        self.assertIn('accounts', response.context)
        
    def test_accounts_list_with_sorting(self):
        """Test accounts list with sorting parameters"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard:accounts_list'), {
            'sort': 'name',
            'order': 'desc'
        })
        self.assertEqual(response.status_code, 200)
        
    def test_account_detail_view(self):
        """Test account detail view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard:account_detail', args=[self.account.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/account_detail.html')
        self.assertEqual(response.context['account'], self.account)
        
    def test_account_detail_view_unauthorized(self):
        """Test account detail view for unauthorized user"""
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        other_account = Account.objects.create(
            user=other_user,
            name='Other Account',
            account_type='checking'
        )
        
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard:account_detail', args=[other_account.id]))
        self.assertEqual(response.status_code, 404)  # Not found for unauthorized user
        
    def test_account_create_view_get(self):
        """Test account create view GET request"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard:account_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/account_form.html')
        self.assertIn('form', response.context)
        
    def test_account_create_view_post(self):
        """Test account create view POST request"""
        self.client.login(username='testuser', password='testpass123')
        form_data = {
            'name': 'New Test Account',
            'account_type': 'savings',
            'classification': 'taxable',
            'asset_type': 'cash',
            'currency': 'USD',
            'institution': 'Test Bank',
            'account_number': '987654321'
        }
        response = self.client.post(reverse('dashboard:account_create'), form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        
        # Check if account was created
        account = Account.objects.filter(name='New Test Account').first()
        self.assertIsNotNone(account)
        self.assertEqual(account.user, self.user)
        
    def test_account_edit_view(self):
        """Test account edit view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard:account_edit', args=[self.account.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/account_form.html')
        self.assertEqual(response.context['account'], self.account)
        
    def test_account_delete_view(self):
        """Test account delete view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard:account_delete', args=[self.account.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/account_confirm_delete.html')
        
        # Test actual deletion
        response = self.client.post(reverse('dashboard:account_delete', args=[self.account.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after success
        
        # Check if account is marked as inactive
        self.account.refresh_from_db()
        self.assertFalse(self.account.is_active)


class TransactionViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.account = Account.objects.create(
            user=self.user,
            name='Test Account',
            account_type='checking'
        )
        
    def test_transactions_list_view(self):
        """Test transactions list view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard:transactions_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/transactions_list.html')
        
    def test_transactions_list_with_filters(self):
        """Test transactions list with filters"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard:transactions_list'), {
            'account': self.account.id,
            'category': 'food',
            'transaction_type': 'expense'
        })
        self.assertEqual(response.status_code, 200)
        
    def test_transaction_create_view(self):
        """Test transaction create view"""
        self.client.login(username='testuser', password='testpass123')
        
        # Test GET request
        response = self.client.get(reverse('dashboard:transaction_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/transaction_form.html')
        
        # Test POST request
        form_data = {
            'account': self.account.id,
            'amount': '100.50',
            'transaction_type': 'expense',
            'category': 'food',
            'description': 'Grocery shopping',
            'date': '2024-01-15'
        }
        response = self.client.post(reverse('dashboard:transaction_create'), form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        
        # Check if transaction was created
        transaction = Transaction.objects.filter(description='Grocery shopping').first()
        self.assertIsNotNone(transaction)
        self.assertEqual(transaction.user, self.user)
        self.assertEqual(transaction.account, self.account)
        
    def test_transaction_edit_view(self):
        """Test transaction edit view"""
        transaction = Transaction.objects.create(
            user=self.user,
            account=self.account,
            amount=Decimal('100.50'),
            transaction_type='expense',
            category='food',
            description='Test transaction',
            date=date(2024, 1, 15)
        )
        
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard:transaction_edit', args=[transaction.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/transaction_form.html')
        
    def test_transaction_delete_view(self):
        """Test transaction delete view"""
        transaction = Transaction.objects.create(
            user=self.user,
            account=self.account,
            amount=Decimal('100.50'),
            transaction_type='expense',
            category='food',
            description='Test transaction',
            date=date(2024, 1, 15)
        )
        
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard:transaction_delete', args=[transaction.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/transaction_confirm_delete.html')
        
        # Test actual deletion
        response = self.client.post(reverse('dashboard:transaction_delete', args=[transaction.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after success
        
        # Check if transaction was deleted
        self.assertFalse(Transaction.objects.filter(id=transaction.id).exists())


class AccountEntriesViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.account = Account.objects.create(
            user=self.user,
            name='Test Account',
            account_type='checking'
        )
        
    def test_account_entries_view(self):
        """Test account entries view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard:account_entries'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/account_entries.html')
        
    def test_account_entries_with_month_year(self):
        """Test account entries with specific month/year"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard:account_entries'), {
            'month': 1,
            'year': 2024
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['selected_month'], 1)
        self.assertEqual(response.context['selected_year'], 2024)
        
    def test_account_entries_template_has_auto_submit_js(self):
        """Test that the template includes JavaScript for auto-submit functionality"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard:account_entries'))
        self.assertEqual(response.status_code, 200)
        
        # Check that the template includes the necessary JavaScript
        self.assertContains(response, 'autoSubmit')
        self.assertContains(response, 'monthSelect')
        self.assertContains(response, 'yearSelect')
        self.assertContains(response, 'addEventListener')
        
    def test_account_entries_post(self):
        """Test account entries POST request"""
        self.client.login(username='testuser', password='testpass123')
        
        form_data = {
            f'balance_{self.account.id}': '5000.00',
            f'notes_{self.account.id}': 'Monthly balance update'
        }
        response = self.client.post(reverse('dashboard:account_entries'), form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        
        # Check if entry was created
        entry = AccountEntry.objects.filter(account=self.account).first()
        self.assertIsNotNone(entry)
        self.assertEqual(entry.balance, Decimal('5000.00'))
        self.assertEqual(entry.notes, 'Monthly balance update')

    def test_clear_data_action(self):
        """Test clear data action for account entries"""
        # Create some entries first
        AccountEntry.objects.create(
            account=self.account,
            month=6,
            year=2025,
            balance=Decimal('5000.00'),
            notes='Test notes'
        )
        
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('dashboard:account_entries'), {
            'action': 'clear_data',
            'sort': 'name',
            'order': 'asc',
            'month': 6,
            'year': 2025
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect after success
        
        # Check if entries were cleared
        entry = AccountEntry.objects.filter(account=self.account, month=6, year=2025).first()
        self.assertIsNotNone(entry)
        self.assertEqual(entry.balance, Decimal('0.00'))
        self.assertEqual(entry.notes, '')


class SettingsViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        
    def test_settings_view(self):
        """Test settings view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard:settings'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/settings.html')
        
    def test_settings_update(self):
        """Test settings update"""
        self.client.login(username='testuser', password='testpass123')
        form_data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated@example.com'
        }
        response = self.client.post(reverse('dashboard:settings'), form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        
        # Check if user was updated
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'Name')
        self.assertEqual(self.user.email, 'updated@example.com')


class DataManagementViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.account = Account.objects.create(
            user=self.user,
            name='Test Account',
            account_type='checking'
        )
        
    def test_data_management_view(self):
        """Test data management view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard:data_management'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/data_management.html')
        
    def test_delete_accounts_action(self):
        """Test delete accounts action"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('dashboard:data_management'), {
            'action': 'delete_accounts'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        
        # Check if accounts were deleted
        self.assertFalse(Account.objects.filter(user=self.user).exists())
        
    def test_delete_entries_action(self):
        """Test delete entries action"""
        # Create an entry first
        AccountEntry.objects.create(
            account=self.account,
            month=1,
            year=2024,
            balance=Decimal('5000.00')
        )
        
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('dashboard:data_management'), {
            'action': 'delete_entries'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        
        # Check if entries were deleted
        self.assertFalse(AccountEntry.objects.filter(account__user=self.user).exists())
        
    def test_import_entries_with_month_names(self):
        """Test importing entries with month names and formatted balances"""
        self.client.login(username='testuser', password='testpass123')
        
        # Create test CSV content with month names and formatted balances
        csv_content = """account_name,month,year,balance,notes
Test Account,January,2025,"61,188.30",Test note 1
Test Account,February,2025,"61,881.49",Test note 2
Test Account,March,2025,"62,381.49",Test note 3"""
        
        # Create a mock file
        from django.core.files.uploadedfile import SimpleUploadedFile
        csv_file = SimpleUploadedFile(
            "test_entries.csv",
            csv_content.encode('utf-8'),
            content_type='text/csv'
        )
        
        response = self.client.post(reverse('dashboard:data_management'), {
            'action': 'import_entries',
            'csv_file': csv_file
        })
        
        self.assertEqual(response.status_code, 200)
        
        # Check if entries were created with correct month numbers
        entries = AccountEntry.objects.filter(account=self.account)
        self.assertEqual(entries.count(), 3)
        
        # Check specific entries
        jan_entry = entries.filter(month=1, year=2025).first()
        self.assertIsNotNone(jan_entry)
        self.assertEqual(jan_entry.balance, Decimal('61188.30'))
        
        feb_entry = entries.filter(month=2, year=2025).first()
        self.assertIsNotNone(feb_entry)
        self.assertEqual(feb_entry.balance, Decimal('61881.49'))
        
        mar_entry = entries.filter(month=3, year=2025).first()
        self.assertIsNotNone(mar_entry)
        self.assertEqual(mar_entry.balance, Decimal('62381.49'))


class ExportViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.account = Account.objects.create(
            user=self.user,
            name='Test Account',
            account_type='checking'
        )
        
    def test_export_csv_accounts(self):
        """Test CSV export for accounts"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard:export_csv', args=['accounts']))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        
    def test_export_csv_transactions(self):
        """Test CSV export for transactions"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard:export_csv', args=['transactions']))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        
    def test_export_csv_entries(self):
        """Test CSV export for entries"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard:export_csv', args=['entries']))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        
    def test_export_csv_invalid_type(self):
        """Test CSV export with invalid data type"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard:export_csv', args=['invalid']))
        self.assertEqual(response.status_code, 400)
        
    def test_export_excel_accounts(self):
        """Test Excel export for accounts"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard:export_excel', args=['accounts']))
        self.assertEqual(response.status_code, 200)
        self.assertIn('spreadsheetml', response['Content-Type'])
        
    def test_export_pdf_accounts(self):
        """Test PDF export for accounts"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard:export_pdf', args=['accounts']))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')


class StaticPagesTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_support_page(self):
        """Test support page"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard:support'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/support.html')
        
    def test_terms_of_service_page(self):
        """Test terms of service page"""
        response = self.client.get(reverse('dashboard:terms_of_service'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/terms_of_service.html')
        
    def test_privacy_policy_page(self):
        """Test privacy policy page"""
        response = self.client.get(reverse('dashboard:privacy_policy'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/privacy_policy.html')


class IntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_complete_workflow(self):
        """Test complete workflow: create account, add entry, add transaction"""
        self.client.login(username='testuser', password='testpass123')
        
        # 1. Create an account
        account_data = {
            'name': 'Test Account',
            'account_type': 'checking',
            'classification': 'taxable',
            'asset_type': 'cash',
            'currency': 'USD',
            'institution': 'Test Bank'
        }
        response = self.client.post(reverse('dashboard:account_create'), account_data)
        self.assertEqual(response.status_code, 302)
        
        account = Account.objects.get(name='Test Account')
        
        # 2. Add account entry
        entry_data = {
            f'balance_{account.id}': '5000.00',
            f'notes_{account.id}': 'Initial balance'
        }
        response = self.client.post(reverse('dashboard:account_entries'), entry_data)
        self.assertEqual(response.status_code, 302)
        
        # 3. Add transaction
        transaction_data = {
            'account': account.id,
            'amount': '100.50',
            'transaction_type': 'expense',
            'category': 'food',
            'description': 'Grocery shopping',
            'date': '2024-01-15'
        }
        response = self.client.post(reverse('dashboard:transaction_create'), transaction_data)
        self.assertEqual(response.status_code, 302)
        
        # 4. Verify data exists
        self.assertTrue(Account.objects.filter(name='Test Account').exists())
        self.assertTrue(AccountEntry.objects.filter(account=account).exists())
        self.assertTrue(Transaction.objects.filter(account=account).exists())
        
        # 5. Check dashboard shows correct data
        response = self.client.get(reverse('dashboard:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('total_balance', response.context)
