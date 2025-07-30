from django.contrib import admin
from .models import Account, Transaction, AccountEntry


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'account_type', 'classification', 'asset_type', 'currency', 'institution', 'is_active', 'created_at']
    list_filter = ['account_type', 'classification', 'asset_type', 'currency', 'is_active', 'created_at']
    search_fields = ['name', 'user__username', 'institution']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Account Information', {
            'fields': ('user', 'name', 'account_type', 'classification', 'asset_type', 'currency')
        }),
        ('Additional Details', {
            'fields': ('institution', 'account_number', 'is_active'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['description', 'user', 'account', 'amount', 'transaction_type', 'category', 'date', 'created_at']
    list_filter = ['transaction_type', 'category', 'date', 'created_at']
    search_fields = ['description', 'user__username', 'account__name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Transaction Details', {
            'fields': ('user', 'account', 'amount', 'transaction_type', 'category', 'description', 'date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AccountEntry)
class AccountEntryAdmin(admin.ModelAdmin):
    list_display = ['account', 'month', 'year', 'balance', 'created_at']
    list_filter = ['month', 'year', 'created_at']
    search_fields = ['account__name', 'account__user__username']
    list_editable = ['balance']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Entry Information', {
            'fields': ('account', 'month', 'year', 'balance', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )