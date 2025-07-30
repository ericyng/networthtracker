from django import forms
from .models import Account, Transaction, AccountEntry


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'account_type', 'classification', 'asset_type', 'currency', 'institution', 'account_number']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Account Name'}),
            'account_type': forms.Select(attrs={'class': 'form-control'}),
            'classification': forms.Select(attrs={'class': 'form-control'}),
            'asset_type': forms.Select(attrs={'class': 'form-control'}),
            'currency': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'USD'}),
            'institution': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bank Name (optional)'}),
            'account_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Account Number (optional)'}),
        }


class AccountEntryForm(forms.ModelForm):
    class Meta:
        model = AccountEntry
        fields = ['month', 'year', 'balance', 'notes']
        widgets = {
            'month': forms.Select(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'min': '2020', 'max': '2030'}),
            'balance': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional notes about this entry'}),
        }


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['account', 'amount', 'transaction_type', 'category', 'description', 'date']
        widgets = {
            'account': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'transaction_type': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Transaction Description'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['account'].queryset = Account.objects.filter(user=user, is_active=True)


 