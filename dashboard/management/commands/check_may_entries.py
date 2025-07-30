from django.core.management.base import BaseCommand
from dashboard.models import AccountEntry, Account


class Command(BaseCommand):
    help = 'Check account entries for May 2025'

    def handle(self, *args, **options):
        # Check for May 2025 entries
        may_entries = AccountEntry.objects.filter(month=5, year=2025).select_related('account')
        
        self.stdout.write(f'Found {may_entries.count()} entries for May 2025:')
        
        for entry in may_entries:
            self.stdout.write(
                f'  Account: {entry.account.name} (ID: {entry.account.id}), '
                f'Balance: ${entry.balance}, Notes: "{entry.notes}", '
                f'Entry ID: {entry.id}'
            )
        
        # Check for duplicate accounts
        accounts = Account.objects.all()
        account_names = {}
        for account in accounts:
            if account.name in account_names:
                self.stdout.write(
                    self.style.WARNING(
                        f'DUPLICATE ACCOUNT NAME: "{account.name}" - '
                        f'IDs: {account_names[account.name]}, {account.id}'
                    )
                )
            else:
                account_names[account.name] = [account.id]
        
        # Check total accounts
        self.stdout.write(f'\nTotal accounts: {accounts.count()}')
        self.stdout.write(f'Total May 2025 entries: {may_entries.count()}') 