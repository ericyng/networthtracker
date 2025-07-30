from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from dashboard.models import AccountEntry, Account
from django.db.models import Sum


class Command(BaseCommand):
    help = 'Check dashboard graph data for the last 12 months'

    def handle(self, *args, **options):
        # Get the current month and year
        current_date = timezone.now()
        
        self.stdout.write(f'Current date: {current_date}')
        self.stdout.write('Checking dashboard data calculation:\n')
        
        chart_data = []
        line_chart_data = []
        
        # Generate data for the last 12 months (same logic as dashboard view)
        for i in range(11, -1, -1):  # 11 to 0 (last 12 months)
            # Calculate the target month properly
            target_month = current_date.month - i
            target_year = current_date.year
            
            # Handle month rollover
            while target_month <= 0:
                target_month += 12
                target_year -= 1
            
            month = target_month
            year = target_year
            
            month_names = ['January', 'February', 'March', 'April', 'May', 'June', 
                          'July', 'August', 'September', 'October', 'November', 'December']
            month_name = month_names[month-1]
            self.stdout.write(f'Month {i}: {month_name} {year} (Month: {month}, Year: {year})')
            
            # Get total balance for this month/year (for bar chart)
            monthly_balance = AccountEntry.objects.filter(
                month=month,
                year=year
            ).aggregate(total=Sum('balance'))['total'] or 0
            
            # Get detailed breakdown for line chart
            monthly_entries = AccountEntry.objects.filter(
                month=month,
                year=year
            ).select_related('account')
            
            # Calculate assets, debts, and net worth for this month
            monthly_assets = 0
            monthly_debts = 0
            
            for entry in monthly_entries:
                if entry.account.classification == 'debts' or entry.account.account_type == 'loan':
                    monthly_debts += entry.balance
                else:
                    monthly_assets += entry.balance
            
            monthly_net_worth = monthly_assets + monthly_debts  # debts are negative
            
            # Create proper month label
            month_abbrevs = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            month_label = f"{month_abbrevs[month-1]} {year}"
            
            chart_data.append({
                'month': month_label,
                'balance': float(monthly_balance),
                'month_num': month,
                'year': year
            })
            
            line_chart_data.append({
                'month': month_label,
                'net_worth': float(monthly_net_worth),
                'assets': float(monthly_assets),
                'debts': float(abs(monthly_debts)),  # Show as positive for display
                'month_num': month,
                'year': year
            })
            
            self.stdout.write(f'  Balance: ${monthly_balance:,.2f}')
            self.stdout.write(f'  Net Worth: ${monthly_net_worth:,.2f}')
            self.stdout.write(f'  Assets: ${monthly_assets:,.2f}')
            self.stdout.write(f'  Debts: ${abs(monthly_debts):,.2f}')
            self.stdout.write(f'  Entries count: {monthly_entries.count()}')
            self.stdout.write('')
        
        # Check for duplicate months in the data
        month_labels = [item['month'] for item in chart_data]
        duplicates = {}
        for i, label in enumerate(month_labels):
            if label in duplicates:
                duplicates[label].append(i)
            else:
                duplicates[label] = [i]
        
        duplicate_months = {label: indices for label, indices in duplicates.items() if len(indices) > 1}
        
        if duplicate_months:
            self.stdout.write(self.style.WARNING('DUPLICATE MONTHS FOUND:'))
            for month, indices in duplicate_months.items():
                self.stdout.write(f'  {month}: appears at indices {indices}')
                for idx in indices:
                    self.stdout.write(f'    Index {idx}: Balance ${chart_data[idx]["balance"]:,.2f}')
        else:
            self.stdout.write(self.style.SUCCESS('No duplicate months found in chart data')) 