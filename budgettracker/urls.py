from django.urls import path

from budgettracker.models import Account
from . import views

urlpatterns = [
    path('', views.index),
    path('accounts', views.AccountView.as_view()),
    path('accounts/<account_name>', views.AccountView.as_view()),
    path('accounts/<account_name>/transactions', views.TransactionView.as_view()),
    path('accounts/<account_name>/transactions/<transaction_id>', views.TransactionView.as_view()),
]