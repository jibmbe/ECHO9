# models.py
# models.py
from django.contrib.auth.models import User
from django.db import models
import random
import string

INVESTMENT_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('completed', 'Completed'),
    ('rejected', 'Rejected'),
]

WITHDRAWAL_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('completed', 'Completed'),
    ('rejected', 'Rejected'),
]

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    level_one_bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    level_two_bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    level_three_bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    referral_link = models.CharField(max_length=100, unique=True, blank=True, null=True)
    inviter = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='invited_users')
    referred_users = models.ManyToManyField('self', blank=True)
    withdrawal_request_pending = models.BooleanField(default=False)
    investment = models.ForeignKey('Investment', on_delete=models.SET_NULL, null=True, blank=True, related_name='user_investment')
    coin_wallet = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    is_active = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.referral_link:
            self.referral_link = self.generate_referral_link()
            print(f"DEBUG: Generating referral link for {self.user.username}: {self.referral_link}")
        super(UserProfile, self).save(*args, **kwargs)

    def generate_referral_link(self):
        user_id_str = str(self.user.id)
        random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        return f'{user_id_str}-{random_chars}'

    def activate_account(self):
        self.is_active = True
        self.save()

class DepositWallet(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

class WithdrawalWallet(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=WITHDRAWAL_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    is_pending = models.BooleanField(default=True)

    def _str_(self):
        return f"{self.user.user.username} - ${self.amount} - {self.status}"

class SpinWallet(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

class Withdrawal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.user.username} - ${self.amount} - {self.timestamp}"

class Investment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='investments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=INVESTMENT_STATUS_CHOICES, default='pending')
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    maturity_days = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    matured_at = models.DateTimeField(null=True, blank=True)

    def _str_(self):
        return f"Investment #{self.id} - {self.user.user.username}"

class InvestmentWallet(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=INVESTMENT_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    is_pending = models.BooleanField(default=True)

    def _str_(self):
        return f"{self.user.user.username} - ${self.amount} - {self.status}"

class Referral(models.Model):
    referring_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='referrals_given')
    referred_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='referrals_received')

    def _str_(self):
        return f"{self.referring_user.user.username} referred {self.referred_user.user.username}"

class EchoCoin(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)

class CoinOrder(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    coin = models.ForeignKey(EchoCoin, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    order_type = models.CharField(max_length=4, choices=[('buy', 'Buy'), ('sell', 'Sell')])
    timestamp = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.user_profile.user.username} - {self.order_type} - {self.amount} coins at ${self.price}"

class CoinTransaction(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    coin = models.ForeignKey(EchoCoin, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=4, choices=[('buy', 'Buy'), ('sell', 'Sell')])
    timestamp = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.user_profile.user.username} - {self.transaction_type} - {self.amount} coins"
    
class Pledge(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)  # Set a default value for created_at
    status = models.CharField(max_length=20, default='active')
    

class Sale(models.Model):
    buyer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='buyer_sales')
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='seller_sales')
    pledge = models.ForeignKey(Pledge, on_delete=models.CASCADE)
    profit = models.DecimalField(max_digits=10, decimal_places=2)