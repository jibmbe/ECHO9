from django.urls import path
from .views import create_pledge, deposit, home, list_pledges, list_transactions, pair_pledges, referred_users, register_user, trade_coins, user_login, user_wallet, withdraw_funds
from . import views 


urlpatterns = [

    path('register/', register_user, name='register_user'),
    path('user_wallet/', user_wallet, name='user_wallet'),
    path('login/', user_login, name='user_login'), 
    path('referred_users/', referred_users, name='referred_users'),
    path('withdraw_funds/', withdraw_funds, name='withdraw_funds'),
    path('deposit/', deposit, name='deposit'),
    path('invest/', views.invest, name='invest'),
    path('', home, name='home'),
    path('trade_coins/', trade_coins, name='trade_coins'),
    path('create_pledge/', create_pledge, name='create_pledge'),
    path('list_pledges/', list_pledges, name='list_pledges'),
    path('pair_pledges/<int:pledge_id>/', pair_pledges, name='pair_pledges'),
    path('List_transactions/', list_transactions, name='list_transactions'),
    
]