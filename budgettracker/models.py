# from django.conf import settings
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# Create your models here.
class Account(models.Model):
    name = models.CharField(max_length=10, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Transaction(models.Model):

    class Categories(models.IntegerChoices):
        ENTERTAINMENT = 0
        FOOD = 1
        UTILITY = 2
        BILL = 3
        SHOPPING = 4

    class Kind(models.IntegerChoices):
        CREDIT = 0
        DEBIT = 1

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    category = models.IntegerField(choices=Categories.choices, default=Categories.SHOPPING)
    amount = models.IntegerField(default=0, validators=[MinValueValidator(0, "Amount should not be less than zero!")])
    kind = models.IntegerField(choices=Kind.choices, default=Kind.DEBIT)
    processed_at = models.DateField()
    created_at = models.DateField(auto_now_add=True)
    last_modified_at = models.DateField(auto_now=True)

class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['account', 'category', 'amount', 'kind', 'processed_at']

class AcccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'user']
