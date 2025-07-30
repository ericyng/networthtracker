from django.core.management.base import BaseCommand
from django.utils import timezone
from dashboard.models import AccountEntry, Account
from django.db.models import Sum


class Command(BaseCommand):
    help = 'Test the combination chart data structure with net worth line overlay'

    def handle(self, *args, **options):
        # Get the current month and year
        current_date = timezone.now()
        
        self.stdout.write(f'Testing combination chart data structure for current month ({current_date.month}/{current_date.year}):\n')
        
        # Get current month entries
        current_entries = AccountEntry.objects.filter(
            month=current_date.month,
            year=current_date.year
        ).select_related('account')
        
        if not current_entries.exists():
            self.stdout.write('No entries found for current month.')
            return
        
        # Calculate category breakdown
        monthly_categories = {
            'cash': 0,
            'equity_investments': 0,
            'retirement': 0,
            'property': 0,
            'debts': 0,
            'other': 0
        }
        
        for entry in current_entries:
            account = entry.account
            balance = entry.balance
            
            # Determine category based on account type and classification
            if account.account_type in ['checking', 'savings']:
                monthly_categories['cash'] += balance
            elif account.account_type == 'investment' and account.classification not in ['pretax', 'posttax', 'roth', 'traditional', '401k', 'hsa', '529', 'fsa']:
                monthly_categories['equity_investments'] += balance
            elif account.classification in ['pretax', 'posttax', 'roth', 'traditional', '401k', 'hsa', '529', 'fsa']:
                monthly_categories['retirement'] += balance
            elif account.asset_type == 'property':
                monthly_categories['property'] += balance
            elif account.classification == 'debts' or account.account_type in ['loan', 'credit']:
                monthly_categories['debts'] += balance
            else:
                monthly_categories['other'] += balance
        
        # Calculate net worth
        monthly_net_worth = sum(monthly_categories.values())
        
        self.stdout.write('=== COMBINATION CHART DATA ===')
        self.stdout.write('Category Breakdown for Stacked Bars:')
        self.stdout.write(f'  Cash: ${monthly_categories["cash"]:,.2f}')
        self.stdout.write(f'  Equity & Investments: ${monthly_categories["equity_investments"]:,.2f}')
        self.stdout.write(f'  Retirement: ${monthly_categories["retirement"]:,.2f}')
        self.stdout.write(f'  Property: ${monthly_categories["property"]:,.2f}')
        self.stdout.write(f'  Debts: ${monthly_categories["debts"]:,.2f}')
        self.stdout.write(f'  Other: ${monthly_categories["other"]:,.2f}')
        
        self.stdout.write(f'\nNet Worth Line Overlay:')
        self.stdout.write(f'  Net Worth: ${monthly_net_worth:,.2f}')
        
        self.stdout.write('\n=== CHART DATA STRUCTURE ===')
        self.stdout.write('Sample combination chart data point:')
        chart_data_point = {
            'month': f"{current_date.strftime('%b')} {current_date.year}",
            'balance': float(sum(monthly_categories.values())),
            'net_worth': float(monthly_net_worth),
            'cash': float(monthly_categories['cash']),
            'equity_investments': float(monthly_categories['equity_investments']),
            'retirement': float(monthly_categories['retirement']),
            'property': float(monthly_categories['property']),
            'debts': float(monthly_categories['debts']),
            'other': float(monthly_categories['other']),
            'month_num': current_date.month,
            'year': current_date.year
        }
        
        for key, value in chart_data_point.items():
            if isinstance(value, float):
                self.stdout.write(f'  {key}: ${value:,.2f}')
            else:
                self.stdout.write(f'  {key}: {value}')
        
        self.stdout.write('\n=== CHART CONFIGURATION ===')
        self.stdout.write('Chart Type: Combination (Stacked Bar + Line)')
        self.stdout.write('Bar Datasets: 6 (Cash, Equity & Investments, Retirement, Property, Debts, Other)')
        self.stdout.write('Line Dataset: 1 (Net Worth)')
        self.stdout.write('Net Worth Line Color: rgba(75, 192, 192, 1) - Teal')
        self.stdout.write('Net Worth Line Width: 3px')
        self.stdout.write('Net Worth Line Tension: 0.4') 