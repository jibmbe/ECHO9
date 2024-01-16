
import decimal
from gettext import translation
import secrets
import uuid
from venv import logger
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.test import TransactionTestCase
from echo9_app.forms import CoinTransactionForm, CustomUserCreationForm, DepositForm, InvestmentForm, PledgeForm, WithdrawalForm
from .models import CoinTransaction, Investment, InvestmentWallet, Pledge, Sale, UserProfile, DepositWallet, WithdrawalWallet, SpinWallet
from django.contrib import messages

def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Create a UserProfile object for the new user
            user_profile = UserProfile.objects.create(user=user, account_balance=0.0)

            # Process referral code
            referral_code = request.POST.get('referral_code')
            if referral_code:
                try:
                    inviter = UserProfile.objects.get(referral_link=referral_code)
                    user_profile.inviter = inviter
                    user_profile.save()

                    # Add the new user to the inviter's list of referred users
                    inviter.referred_users.add(user_profile)
                    inviter.save()

                    # Calculate and update affiliate bonuses for inviter
                    inviter.level_one_bonus += 700
                    inviter.account_balance += 700
                    inviter.save()

                    # Level two bonus
                    if inviter.inviter:
                        inviter.inviter.level_two_bonus += 700
                        inviter.inviter.account_balance += 700
                        inviter.inviter.save()

                        # Level three bonus
                        if inviter.inviter.inviter:
                            inviter.inviter.inviter.level_three_bonus += 1100
                            inviter.inviter.inviter.account_balance += 1100
                            inviter.inviter.inviter.save()

                except UserProfile.DoesNotExist:
                    pass  # Handle invalid referral code

            # Ensure that the user is logged in after registration
            login(request, user)
            return redirect('user_wallet')

    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

def user_wallet(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user_profile = get_object_or_404(UserProfile, user=request.user)

    deposit_wallet = DepositWallet.objects.filter(user=user_profile)
    withdrawal_wallet = WithdrawalWallet.objects.filter(user=user_profile)
    investment_wallet = InvestmentWallet.objects.filter(user=user_profile)
    spin_wallet = SpinWallet.objects.filter(user=user_profile)
    coin_wallet = CoinTransaction.objects.filter(user_profile=user_profile)

    referred_users = user_profile.referred_users.all()

    if not user_profile.is_active:
        if request.method == 'POST':
            entered_code = request.POST.get('verification_code')
            correct_code = request.session.get('verification_code')

            if entered_code == correct_code:
                user_profile.is_active = True
                user_profile.save()
                messages.success(request, 'Account activated successfully!')
            else:
                messages.error(request, 'Incorrect verification code. Please try again.')

            return redirect('user_wallet')

        # Generate a random verification code and store it in the session
        verification_code = secrets.token_hex(6).upper()  # Adjust the length as needed
        request.session['verification_code'] = verification_code

        return render(request, 'enter_verification_code.html', {'verification_code': verification_code})

    # User's account is activated, proceed with the wallet view
    return render(request, 'user_wallet.html', {
        'user_profile': user_profile,
        'referred_users': referred_users,
        'deposit_wallet': deposit_wallet,
        'withdrawal_wallet': withdrawal_wallet,
        'investment_wallet': investment_wallet,
        'spin_wallet': spin_wallet,
        'coin_wallet': coin_wallet,
    })

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                # Set the inviter's ID in the session
                if 'inviter_id' in request.GET:
                    request.session['inviter_id'] = request.GET['inviter_id']

                return redirect('user_wallet')

    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})

@login_required
def referred_users(request):
    user_profile = UserProfile.objects.get(user=request.user)
    referred_users = user_profile.referred_users.all()
    return render(request, 'referred_users.html', {'referred_users': referred_users})

@login_required
def withdraw_funds(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            withdrawal_amount = form.cleaned_data['amount']

            # Check if the user has sufficient funds in the account balance
            if user_profile.account_balance >= withdrawal_amount:
                # Deduct the withdrawal amount from the account balance
                user_profile.account_balance -= withdrawal_amount
                user_profile.save()

                # Create the withdrawal wallet entry
                withdrawal_wallet = WithdrawalWallet.objects.create(
                    user=user_profile,
                    amount=withdrawal_amount,
                    status='pending',  # Set the default status for pending withdrawals
                    is_pending=True,
                )

                return redirect('user_wallet')
            else:
                # Provide an error message for insufficient funds
                error_message = "Insufficient funds in the account balance."
                return render(request, 'withdraw_funds.html', {'error_message': error_message, 'form': form})
    else:
        form = WithdrawalForm()

    return render(request, 'withdraw_funds.html', {'form': form, 'username': request.user.username})


@login_required
def withdrawal_request(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            withdrawal = form.save(commit=False)
            withdrawal.user = user_profile
            withdrawal.save()
            messages.success(request, 'Withdrawal request submitted successfully.')
            return redirect('user_wallet')
    else:
        form = WithdrawalForm()

    withdrawal_history = WithdrawalWallet.objects.filter(user=user_profile)

    return render(request, 'withdrawal_request.html', {'form': form, 'withdrawal_history': withdrawal_history})

@login_required
def deposit(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            deposit_option = form.cleaned_data['deposit_option']

            if deposit_option == 'account_balance':
                # Deposit from account balance
                if user_profile.account_balance >= amount:
                    user_profile.account_balance -= amount
                    user_profile.save()
                    DepositWallet.objects.create(user=user_profile, amount=amount)
                    messages.success(request, f'Successfully deposited ${amount} from account balance.')
                else:
                    messages.error(request, 'Insufficient funds in account balance.')
            elif deposit_option == 'mpesa':
                # Handle M-Pesa deposit logic here
                # You may want to integrate with an external API or simulate the process

                # For simulation purposes, assume the M-Pesa deposit was successful
                DepositWallet.objects.create(user=user_profile, amount=amount)
                messages.success(request, f'Successfully deposited ${amount} from M-Pesa.')
            else:
                messages.error(request, 'Invalid deposit option.')

            return redirect('user_wallet')

    else:
        form = DepositForm()

    return render(request, 'deposit.html', {'form': form})


@login_required
def initiate_withdrawal(request):
    if request.method == 'POST':
        form = WithdrawalForm(request.POST)  # Use your form
        if form.is_valid():
            withdrawal_amount = form.cleaned_data['amount']
            withdrawal_instance = WithdrawalWallet.objects.create(user=request.user.userprofile, amount=withdrawal_amount, status='pending')
            return redirect('withdrawal_success')  # Redirect to a success page or handle accordingly
    else:
        form = WithdrawalForm()  # Use your form

    return render(request, 'withdrawal.html', {'form': form})

@login_required
def invest(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = InvestmentForm(request.POST)
        if form.is_valid():
            investment_amount = form.cleaned_data['amount']

            # Check if the user has sufficient funds in the account balance
            if user_profile.account_balance >= investment_amount:
                # Deduct the investment amount from the account balance
                user_profile.account_balance -= investment_amount
                user_profile.save()

                # Create the investment
                investment = form.save(commit=False)
                investment.user = user_profile
                investment.save()

                # Redirect to user_wallet or provide a success message
                return redirect('user_wallet')
            else:
                # Provide an error message for insufficient funds
                error_message = "Insufficient funds in the account balance."
                return render(request, 'invest.html', {'error_message': error_message, 'form': form})
        else:
            # Handle the case where the form is not valid
            return render(request, 'invest.html', {'form': form})
    else:
        form = InvestmentForm()

    return render(request, 'invest.html', {'form': form})

def home(request):
    return render(request, 'base.html')

@login_required
def trade_coins(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = CoinTransactionForm(request.POST)
        if form.is_valid():
            coin_transaction = form.save(commit=False)
            coin_transaction.user_profile = user_profile  # Update to use user_profile instead of user

            if coin_transaction.transaction_type == 'buy':
                # Buying logic
                buy_amount = coin_transaction.amount * coin_transaction.buy_price  # Use buy_price

                if user_profile.account_balance >= buy_amount:
                    user_profile.account_balance -= buy_amount
                    user_profile.coin_wallet += coin_transaction.amount
                    user_profile.save()  # Save the changes to the user_profile after buying
                else:
                    messages.error(request, 'Insufficient funds in the account.')
                    return render(request, 'trade_coins.html', {'form': form})

            elif coin_transaction.transaction_type == 'sell':
                # Selling logic
                if user_profile.coin_wallet >= coin_transaction.amount:
                    # Check if there are matching buy orders
                    matching_buy_orders = CoinTransaction.objects.filter(
                        transaction_type='buy',
                        buy_price__gte=coin_transaction.sell_price  # Use buy_price
                    ).order_by('timestamp')

                    if matching_buy_orders.exists():
                        # Execute the sale with the earliest matching buy order
                        buyer_profile = matching_buy_orders.first().user_profile
                        sell_amount = coin_transaction.amount * coin_transaction.sell_price  # Use sell_price

                        buyer_profile.coin_wallet += coin_transaction.amount
                        buyer_profile.account_balance -= sell_amount
                        user_profile.coin_wallet -= coin_transaction.amount
                        user_profile.account_balance += sell_amount

                        buyer_profile.save()
                        user_profile.save()

                        # Remove the matched buy order
                        matching_buy_orders.first().delete()
                    else:
                        messages.error(request, 'No matching buy orders.')
                        return render(request, 'trade_coins.html', {'form': form})

                else:
                    messages.error(request, 'Insufficient coins in the wallet.')
                    return render(request, 'trade_coins.html', {'form': form})

            coin_transaction.save()

            return redirect('user_wallet')  # Redirect to user wallet or a relevant page

    else:
        form = CoinTransactionForm()

    return render(request, 'trade_coins.html', {'form': form})


def create_pledge(request):
    if request.method == 'POST':
        form = PledgeForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            user = request.user.userprofile  # Assuming the user is authenticated
            pledge = Pledge.objects.create(user=user, amount=amount)
            messages.success(request, 'Pledge created successfully!')
            return redirect('list_pledges')
    else:
        form = PledgeForm()
    return render(request, 'pledges/create_pledge.html', {'form': form})

def list_pledges(request):
    # Get all active pledges
    pledges = Pledge.objects.filter(status='active')
    
    # Get user profiles for sellers
    sellers = UserProfile.objects.filter(pledge__in=pledges).distinct()
    
    return render(request, 'pledges/list_pledges.html', {'pledges': pledges, 'sellers': sellers})

def pair_pledges(request, pledge_id):
    pledge = Pledge.objects.get(id=pledge_id)
    
    # Assume the buyer is the user who created the pledge
    buyer = request.user.userprofile
    
    # Ensure the seller is not the buyer
    if buyer == pledge.user:
        messages.error(request, 'You cannot buy a pledge from yourself.')
        return redirect('list_pledges')

    # Calculate profit for the seller
    profit = calculate_profit(pledge.amount)
    
    # Create a Sale instance
    sale = Sale.objects.create(buyer=buyer, seller=pledge.user, pledge=pledge, profit=profit)
    
    # Update pledge status
    pledge.status = 'completed'
    pledge.save()
    
    messages.success(request, 'Pledge paired successfully!')
    
    # Debugging: Add a print statement
    print('Redirecting to list_pledges')
    
    return redirect('list_pledges')

def list_transactions(request):
    user_profile = request.user.userprofile  # Assuming request.user is a User instance with a related UserProfile
    transactions_bought = TransactionTestCase.objects.filter(buyer=user_profile)
    transactions_sold = translation.objects.filter(seller=user_profile)
    
    return render(request, 'pledges/list_transactions.html', {'transactions_bought': transactions_bought, 'transactions_sold': transactions_sold})

def calculate_profit(amount):

    amount_decimal = decimal.Decimal(amount)

    return amount_decimal * decimal.Decimal('0.10')