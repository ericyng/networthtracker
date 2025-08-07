from django.contrib import admin
from .models import Account, Transaction, AccountEntry


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'account_type', 'classification', 'asset_type', 'is_active', 'created_at']
    list_filter = ['account_type', 'classification', 'asset_type', 'is_active', 'created_at']
    search_fields = ['name', 'user__username', 'user__email', 'institution']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'name', 'account_type', 'classification', 'asset_type')
        }),
        ('Financial Details', {
            'fields': ('currency', 'institution', 'account_number')
        }),
        ('Status', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['description', 'user', 'account', 'amount', 'transaction_type', 'category', 'date']
    list_filter = ['transaction_type', 'category', 'date', 'created_at']
    search_fields = ['description', 'user__username', 'user__email', 'account__name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Transaction Details', {
            'fields': ('user', 'account', 'amount', 'transaction_type', 'category')
        }),
        ('Description', {
            'fields': ('description', 'date')
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
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Entry Details', {
            'fields': ('account', 'month', 'year', 'balance')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
