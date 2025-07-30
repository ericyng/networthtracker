from django.core.management.base import BaseCommand
from dashboard.models import Account, AccountEntry
from decimal import Decimal


class Command(BaseCommand):
    help = 'Test the new account grouping logic'

    def handle(self, *args, **options):
        accounts = Account.objects.filter(is_active=True)
        
        self.stdout.write(f'Testing account grouping for {accounts.count()} accounts:\n')
        
        # Test the grouping logic
        accounts_by_category = {}
        category_totals = {}
        
        for account in accounts:
            balance = account.get_latest_balance()
            
            # Determine category based on account type and classification
            if account.account_type in ['checking', 'savings']:
                category = 'Cash'
            elif account.account_type == 'investment' and account.classification not in ['pretax', 'posttax', 'roth', 'traditional', '401k', 'hsa', '529', 'fsa']:
                category = 'Equity & Investments'
            elif account.classification in ['pretax', 'posttax', 'roth', 'traditional', '401k', 'hsa', '529', 'fsa']:
                category = 'Retirement'
            elif account.asset_type == 'property':
                category = 'Property'
            elif account.classification == 'debts' or account.account_type in ['loan', 'credit']:
                category = 'Debts'
            else:
                category = 'Other'
            
            if category not in accounts_by_category:
                accounts_by_category[category] = []
                category_totals[category] = 0
            accounts_by_category[category].append(account)
            category_totals[category] += balance
            
            self.stdout.write(
                f'  {account.name} ({account.account_type}, {account.classification}, {account.asset_type}) '
                f'→ {category} (${balance:,.2f})'
            )
        
        self.stdout.write('\nCategory Summary:')
        for category, accounts_in_group in accounts_by_category.items():
            total = category_totals[category]
            count = len(accounts_in_group)
            self.stdout.write(
                f'  {category}: {count} accounts, Total: ${total:,.2f}'
            )
        
        # Calculate overall totals
        total_balance = sum(category_totals.values())
        total_debts = category_totals.get('Debts', 0)
        total_assets = total_balance - total_debts
        
        self.stdout.write(f'\nOverall Totals:')
        self.stdout.write(f'  Total Assets: ${total_assets:,.2f}')
        self.stdout.write(f'  Total Debts: ${total_debts:,.2f}')
        self.stdout.write(f'  Net Worth: ${total_balance:,.2f}') 