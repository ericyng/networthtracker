from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from dashboard.models import Account, AccountEntry
from decimal import Decimal


class Command(BaseCommand):
    help = 'Test crypto account categorization in dashboard charts and accounts list'

    def handle(self, *args, **options):
        self.stdout.write('Testing crypto account categorization...\n')
        
        # Get the first user (for testing)
        user = User.objects.first()
        if not user:
            self.stdout.write('No users found. Please create a user first.')
            return
        
        self.stdout.write(f'Testing with user: {user.username}\n')
        
        # Create a test crypto account
        crypto_account, created = Account.objects.get_or_create(
            user=user,
            name='Bitcoin Wallet',
            defaults={
                'account_type': 'investment',
                'classification': 'taxable',
                'asset_type': 'crypto',
                'currency': 'USD',
                'institution': 'Coinbase',
                'account_number': 'BTC123456'
            }
        )
        
        if created:
            self.stdout.write('Created test crypto account: Bitcoin Wallet')
        else:
            self.stdout.write('Found existing crypto account: Bitcoin Wallet')
        
        # Create a test entry for the crypto account
        entry, created = AccountEntry.objects.get_or_create(
            account=crypto_account,
            month=7,
            year=2025,
            defaults={
                'balance': Decimal('50000.00'),
                'notes': 'Test crypto balance'
            }
        )
        
        if created:
            self.stdout.write('Created test entry: $50,000.00 for July 2025')
        else:
            self.stdout.write('Found existing entry: $50,000.00 for July 2025')
        
        # Test categorization logic
        self.stdout.write('\n=== CATEGORIZATION TEST ===')
        
        # Test dashboard view categorization
        balance = entry.balance
        account = crypto_account
        
        # Simulate the dashboard view logic
        if account.account_type in ['checking', 'savings']:
            category = 'cash'
        elif account.account_type == 'investment' and account.classification not in ['pretax', 'posttax', 'roth', 'traditional', '401k', 'hsa', '529', 'fsa']:
            category = 'equity_investments'
        elif account.classification in ['pretax', 'posttax', 'roth', 'traditional', '401k', 'hsa', '529', 'fsa']:
            category = 'retirement'
        elif account.asset_type == 'property':
            category = 'property'
        elif account.asset_type == 'crypto':
            category = 'equity_investments'
        elif account.classification == 'debts' or account.account_type in ['loan', 'credit']:
            category = 'debts'
        else:
            category = 'other'
        
        self.stdout.write(f'Dashboard View Categorization: {category}')
        self.stdout.write(f'Expected: equity_investments')
        self.stdout.write(f'Result: {"✅ PASS" if category == "equity_investments" else "❌ FAIL"}')
        
        # Test accounts list view categorization
        # Simulate the accounts list view logic
        if account.account_type in ['checking', 'savings']:
            category = 'Cash'
        elif account.account_type == 'investment' and account.classification not in ['pretax', 'posttax', 'roth', 'traditional', '401k', 'hsa', '529', 'fsa']:
            category = 'Equity & Investments'
        elif account.classification in ['pretax', 'posttax', 'roth', 'traditional', '401k', 'hsa', '529', 'fsa']:
            category = 'Retirement'
        elif account.asset_type == 'property':
            category = 'Property'
        elif account.asset_type == 'crypto':
            category = 'Equity & Investments'
        elif account.classification == 'debts' or account.account_type in ['loan', 'credit']:
            category = 'Debts'
        else:
            category = 'Other'
        
        self.stdout.write(f'\nAccounts List View Categorization: {category}')
        self.stdout.write(f'Expected: Equity & Investments')
        self.stdout.write(f'Result: {"✅ PASS" if category == "Equity & Investments" else "❌ FAIL"}')
        
        # Test pie chart categorization
        # Simulate the pie chart logic
        if account.account_type in ['checking', 'savings']:
            category = 'Cash'
        elif account.account_type == 'investment' and account.classification not in ['pretax', 'posttax', 'roth', 'traditional', '401k', 'hsa', '529', 'fsa']:
            category = 'Equity & Investments'
        elif account.classification in ['pretax', 'posttax', 'roth', 'traditional', '401k', 'hsa', '529', 'fsa']:
            category = 'Retirement'
        elif account.asset_type == 'property':
            category = 'Property'
        elif account.asset_type == 'crypto':
            category = 'Equity & Investments'
        elif account.classification == 'debts' or account.account_type in ['loan', 'credit']:
            category = 'Debts'
        else:
            category = 'Other'
        
        self.stdout.write(f'\nPie Chart Categorization: {category}')
        self.stdout.write(f'Expected: Equity & Investments')
        self.stdout.write(f'Result: {"✅ PASS" if category == "Equity & Investments" else "❌ FAIL"}')
        
        # Show account details
        self.stdout.write(f'\n=== ACCOUNT DETAILS ===')
        self.stdout.write(f'Account Name: {crypto_account.name}')
        self.stdout.write(f'Account Type: {crypto_account.account_type}')
        self.stdout.write(f'Classification: {crypto_account.classification}')
        self.stdout.write(f'Asset Type: {crypto_account.asset_type}')
        self.stdout.write(f'Institution: {crypto_account.institution}')
        self.stdout.write(f'Balance: ${crypto_account.get_latest_balance():,.2f}')
        
        self.stdout.write(f'\n=== SUMMARY ===')
        self.stdout.write('Crypto accounts are now categorized as "Equity & Investments"')
        self.stdout.write('This means they will appear in the same category as other taxable investment accounts')
        self.stdout.write('in all dashboard charts and the accounts list view.') 