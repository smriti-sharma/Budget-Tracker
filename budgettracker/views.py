import json

from django.http.response import Http404, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from .models import (
    Account,
    AcccountForm,
    Transaction,
    TransactionForm
)

def index(request):
    return HttpResponse('Hey')

@method_decorator(csrf_exempt, name='dispatch')
class AccountView(View):
    form_class = AcccountForm

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        if data.get("name", None) not in ["", None]:
            account_name = data["name"]
            try:
                account = Account.objects.get(name=account_name)
                return HttpResponseNotFound(f"Account with {account_name} already exist!")
            except Account.DoesNotExist:
                data['user'] = User.objects.all()[1] # request.user

                form = self.form_class(data)
                if form.is_valid():
                    form.save()
                    return HttpResponse("Success!")

        return HttpResponseBadRequest("Invalid form input!")

    def get(self, request, *args, **kwargs):
        def to_json(account):
            return {
                "name": account.name,
                "user": account.user.get_full_name()
            }

        if kwargs.get("account_name", None) not in ["", None]:
            account_name = kwargs["account_name"]
            try:
                account = Account.objects.get(name=account_name)
                return JsonResponse(to_json(account))
            except Account.DoesNotExist:
                return HttpResponseNotFound(f"Account with {account_name} does not exist!")

        print("args: ", args)
        print("kwargs: ", kwargs)
        return JsonResponse([to_json(x) for x in Account.objects.all()], safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class TransactionView(View):

    form_class = TransactionForm

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        account_name = kwargs.get("account_name", None) or None

        if account_name:
            try:
                account = Account.objects.get(name=account_name)
                data['account'] = account
                form = self.form_class(data)

                if form.is_valid():
                    transaction = form.save()
                    return JsonResponse({"id": transaction.pk})

            except Account.DoesNotExist:
                return HttpResponseNotFound(f"Account with {account_name} does not exist!")

        return HttpResponseBadRequest("Invalid form input!")

    def get(self, request, *args, **kwargs):
        def to_json(transaction):
            return {
                "id": transaction.id,
                "account_name": transaction.account.name,
                "category": transaction.category,
                "amount": transaction.amount,
                "kind": transaction.kind,
                "processed_at": transaction.processed_at
            }   


        account_name = kwargs.get("account_name", None) or None
        transaction_id = kwargs.get("transaction_id", None) or None
        if account_name:
            try:
                # checking if account with the name exists.
                account = Account.objects.get(name=account_name)

                if transaction_id:
                    try:
                        transaction = Transaction.objects.get(pk=transaction_id)
                        return JsonResponse(to_json(transaction))

                    except Transaction.DoesNotExist:
                        return HttpResponseNotFound(f"Transaction with {transaction_id} do not exist!")

                transactions = Transaction.objects.filter(account=account.pk)
                return JsonResponse([to_json(x) for x in transactions], safe=False)

            except Account.DoesNotExist:
                return HttpResponseNotFound(f"Account with {account_name} does not exist!")
    
        return HttpResponseNotFound(f"Invalid input!")
