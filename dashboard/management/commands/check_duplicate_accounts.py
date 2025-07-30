from django.core.management.base import BaseCommand
from dashboard.models import Account


class Command(BaseCommand):
    help = 'Check duplicate Yun\'s IRA accounts'

    def handle(self, *args, **options):
        # Check the two Yun's IRA accounts
        yun_ira_accounts = Account.objects.filter(name="Yun's IRA")
        
        self.stdout.write(f'Found {yun_ira_accounts.count()} accounts named "Yun\'s IRA":')
        
        for account in yun_ira_accounts:
            self.stdout.write(
                f'  ID: {account.id}, '
                f'Type: {account.account_type}, '
                f'Classification: {account.classification}, '
                f'Asset Type: {account.asset_type}, '
                f'Institution: "{account.institution}", '
                f'Account Number: "{account.account_number}", '
                f'Active: {account.is_active}, '
                f'Created: {account.created_at}'
            )
            
            # Check if this account has entries
            entries_count = account.entries.count()
            self.stdout.write(f'    Has {entries_count} entries')
            
            if entries_count > 0:
                latest_entry = account.entries.order_by('-year', '-month').first()
                self.stdout.write(f'    Latest entry: {latest_entry.month}/{latest_entry.year} - ${latest_entry.balance}') 