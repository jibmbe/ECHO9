# echo9_app/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CoinTransaction, Withdrawal, WithdrawalWallet
from .models import Investment

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields



class WithdrawalForm(forms.ModelForm):
    class Meta:
        model = WithdrawalWallet
        fields = '__all__'

class DepositForm(forms.Form):
    amount = forms.DecimalField(min_value=0.01, label='Deposit Amount')
    deposit_option = forms.ChoiceField(choices=[('account_balance', 'Account Balance'), ('mpesa', 'M-Pesa')], widget=forms.RadioSelect)

class InvestmentForm(forms.ModelForm):
    class Meta:
        model = Investment
        fields = ['amount', 'interest_rate', 'maturity_days']

class CoinTransactionForm(forms.ModelForm):
    class Meta:
        model = CoinTransaction
        fields = ['coin', 'amount', 'transaction_type']   


class PledgeForm(forms.Form):
    amount = forms.DecimalField()
    
          