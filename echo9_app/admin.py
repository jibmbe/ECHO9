# admin.py
from django.contrib import admin
from .models import CoinTransaction, EchoCoin, Investment, UserProfile, DepositWallet, Withdrawal, WithdrawalWallet, SpinWallet

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'account_balance','phone_number', 'inviter', 'is_active')  # Include 'is_active' in the list display
    list_filter = ('is_active',)  # Add 'is_active' to the list filter
    actions = ['display_referred_users', 'activate_selected_users']  # Add the 'activate_selected_users' action

    def display_referred_users(self, request, queryset):
        for user_profile in queryset:
            referred_users = user_profile.referred_users.all()
            user_list = ', '.join([user.user.username for user in referred_users])
            self.message_user(request, f"{user_profile.user.username}'s referred users: {user_list}")

    display_referred_users.short_description = "Display referred users"

    def activate_selected_users(self, request, queryset):
        for user_profile in queryset:
            user_profile.activate_account()

        self.message_user(request, f"Selected users activated successfully.")

    activate_selected_users.short_description = "Activate selected users"

class WithdrawalWalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'status', 'created_at', 'is_pending')  # Include 'is_pending' in the list display
    list_filter = ('status', 'is_pending')  # Add 'is_pending' to the list filter
    actions = ['approve_selected_withdrawals']

    def approve_selected_withdrawals(self, request, queryset):
        # Update the status of selected withdrawal records to 'Approved'
        queryset.update(status='Approved')

    approve_selected_withdrawals.short_description = "Approve selected withdrawals"

class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'status', 'created_at', 'matured_at', 'interest_rate', 'maturity_days')
    list_filter = ('status',)
    search_fields = ('user__user__username',) 

admin.site.register(Investment, InvestmentAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(DepositWallet)
admin.site.register(SpinWallet)
admin.site.register(Withdrawal)
admin.site.register(WithdrawalWallet, WithdrawalWalletAdmin)
admin.site.register(EchoCoin)
admin.site.register(CoinTransaction)
