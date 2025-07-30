from django.core.management.base import BaseCommand
from dashboard.models import Account
from collections import defaultdict


class Command(BaseCommand):
    help = 'Clean up duplicate accounts'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fix',
            action='store_true',
            help='Actually delete the duplicate accounts',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without making changes',
        )

    def handle(self, *args, **options):
        # Find accounts with duplicate names
        accounts = Account.objects.all()
        name_groups = defaultdict(list)
        
        for account in accounts:
            name_groups[account.name].append(account)
        
        duplicates = {name: accounts for name, accounts in name_groups.items() if len(accounts) > 1}
        
        if not duplicates:
            self.stdout.write(
                self.style.SUCCESS('No duplicate account names found!')
            )
            return
        
        self.stdout.write(
            self.style.WARNING(f'Found {len(duplicates)} duplicate account names:')
        )
        
        for name, accounts in duplicates.items():
            self.stdout.write(f'\nAccount name: "{name}"')
            for account in accounts:
                status = "ACTIVE" if account.is_active else "INACTIVE"
                entries_count = account.entries.count()
                self.stdout.write(
                    f'  ID: {account.id}, Status: {status}, '
                    f'Type: {account.account_type}, '
                    f'Institution: "{account.institution}", '
                    f'Entries: {entries_count}'
                )
        
        if options['dry_run']:
            self.stdout.write(
                self.style.WARNING('DRY RUN - No changes made')
            )
            return
        
        if not options['fix']:
            self.stdout.write(
                self.style.WARNING(
                    'Use --fix to actually delete the duplicate accounts, or --dry-run to see what would be done'
                )
            )
            return
        
        # Delete duplicate accounts (keep the one with the most entries, or the active one)
        deleted_count = 0
        for name, accounts in duplicates.items():
            # Sort by: 1) active status, 2) number of entries, 3) creation date
            accounts_sorted = sorted(
                accounts,
                key=lambda a: (not a.is_active, -a.entries.count(), a.created_at)
            )
            
            # Keep the first one (best candidate), delete the rest
            to_delete = accounts_sorted[1:]
            
            for account in to_delete:
                self.stdout.write(
                    f'Deleting duplicate account ID {account.id} ("{name}") - '
                    f'Status: {"ACTIVE" if account.is_active else "INACTIVE"}, '
                    f'Entries: {account.entries.count()}'
                )
                account.delete()
                deleted_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully deleted {deleted_count} duplicate accounts!')
        ) 