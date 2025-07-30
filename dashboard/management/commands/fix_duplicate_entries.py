from django.core.management.base import BaseCommand
from django.db.models import Count
from dashboard.models import AccountEntry
from decimal import Decimal


class Command(BaseCommand):
    help = 'Identify and fix duplicate account entries'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fix',
            action='store_true',
            help='Actually fix the duplicates (remove them)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be fixed without making changes',
        )

    def handle(self, *args, **options):
        # Find duplicates
        duplicates = (
            AccountEntry.objects
            .values('account', 'month', 'year')
            .annotate(count=Count('id'))
            .filter(count__gt=1)
            .order_by('account', 'year', 'month')
        )

        if not duplicates:
            self.stdout.write(
                self.style.SUCCESS('No duplicate entries found!')
            )
            return

        self.stdout.write(
            self.style.WARNING(f'Found {len(duplicates)} sets of duplicate entries:')
        )

        total_duplicates = 0
        for dup in duplicates:
            account = dup['account']
            month = dup['month']
            year = dup['year']
            count = dup['count']
            
            # Get the actual duplicate entries
            entries = AccountEntry.objects.filter(
                account_id=account,
                month=month,
                year=year
            ).order_by('created_at')
            
            self.stdout.write(
                f'  Account ID {account}, Month {month}/{year}: {count} entries'
            )
            
            # Show details of each duplicate
            for i, entry in enumerate(entries):
                self.stdout.write(
                    f'    Entry {i+1}: ID {entry.id}, Balance ${entry.balance}, '
                    f'Notes: "{entry.notes}", Created: {entry.created_at}'
                )
            
            total_duplicates += count - 1  # Keep one, remove the rest

        self.stdout.write(f'\nTotal duplicate entries to remove: {total_duplicates}')

        if options['dry_run']:
            self.stdout.write(
                self.style.WARNING('DRY RUN - No changes made')
            )
            return

        if not options['fix']:
            self.stdout.write(
                self.style.WARNING(
                    'Use --fix to actually remove the duplicates, or --dry-run to see what would be done'
                )
            )
            return

        # Fix duplicates by keeping the most recent entry for each account/month/year
        removed_count = 0
        for dup in duplicates:
            account = dup['account']
            month = dup['month']
            year = dup['year']
            
            # Get all entries for this account/month/year, ordered by creation date
            entries = AccountEntry.objects.filter(
                account_id=account,
                month=month,
                year=year
            ).order_by('created_at')
            
            # Keep the first (oldest) entry, remove the rest
            entries_to_remove = entries[1:]
            
            for entry in entries_to_remove:
                self.stdout.write(
                    f'Removing duplicate entry ID {entry.id} for account {account}, '
                    f'month {month}/{year}'
                )
                entry.delete()
                removed_count += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully removed {removed_count} duplicate entries!')
        ) 