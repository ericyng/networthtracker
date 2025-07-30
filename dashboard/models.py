from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Account(models.Model):
    ACCOUNT_TYPES = [
        ('checking', 'Checking'),
        ('savings', 'Savings'),
        ('credit', 'Credit Card'),
        ('investment', 'Investment'),
        ('loan', 'Loan'),
        ('other', 'Other'),
    ]
    
    CLASSIFICATION_TYPES = [
        ('pretax', 'Pre-Tax'),
        ('posttax', 'Post-Tax'),
        ('roth', 'Roth'),
        ('traditional', 'Traditional IRA'),
        ('401k', '401(k)'),
        ('529', '529 Plan'),
        ('hsa', 'HSA'),
        ('fsa', 'FSA'),
        ('taxable', 'Taxable'),
        ('debts', 'Debts'),
        ('other', 'Other'),
    ]
    
    ASSET_TYPES = [
        ('cash', 'Cash & Cash Equivalents'),
        ('property', 'Real Estate'),
        ('vehicles', 'Vehicles'),
        ('jewelry', 'Jewelry & Watches'),
        ('art', 'Art & Collectibles'),
        ('electronics', 'Electronics'),
        ('furniture', 'Furniture & Appliances'),
        ('clothing', 'Clothing & Accessories'),
        ('books', 'Books & Media'),
        ('sports', 'Sports Equipment'),
        ('tools', 'Tools & Equipment'),
        ('other', 'Other Assets'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    classification = models.CharField(max_length=20, choices=CLASSIFICATION_TYPES, default='other')
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPES, default='cash')
    currency = models.CharField(max_length=3, default='USD')
    institution = models.CharField(max_length=100, blank=True)
    account_number = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.account_type}) - {self.user.username}"
    
    def get_latest_balance(self, month=None, year=None):
        """Get the latest balance for a specific month/year or the most recent"""
        if month is None or year is None:
            latest_entry = self.entries.order_by('-year', '-month').first()
        else:
            latest_entry = self.entries.filter(month=month, year=year).first()
        
        return latest_entry.balance if latest_entry else 0.00


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
        ('transfer', 'Transfer'),
    ]
    
    CATEGORIES = [
        ('salary', 'Salary'),
        ('freelance', 'Freelance'),
        ('investment', 'Investment'),
        ('food', 'Food & Dining'),
        ('transportation', 'Transportation'),
        ('housing', 'Housing'),
        ('utilities', 'Utilities'),
        ('entertainment', 'Entertainment'),
        ('shopping', 'Shopping'),
        ('healthcare', 'Healthcare'),
        ('education', 'Education'),
        ('travel', 'Travel'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    description = models.CharField(max_length=200)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
    
    def __str__(self):
        return f"{self.description} - {self.amount} ({self.transaction_type})"


class AccountEntry(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='entries')
    month = models.IntegerField(choices=[(i, i) for i in range(1, 13)])
    year = models.IntegerField()
    balance = models.DecimalField(max_digits=15, decimal_places=2)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-year', '-month']
        unique_together = ['account', 'month', 'year']
    
    def __str__(self):
        return f"{self.account.name} - {self.month}/{self.year}: ${self.balance}"