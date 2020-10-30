from django.shortcuts import render, get_object_or_404
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Account, Transaction
from .serializers import AccountSerializer, TransactionSerializer

class AccountViewSet(viewsets.ModelViewSet):

    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def retrieve(self, request, pk=None):
        queryset = Account.objects.filter(owner__iexact=pk)
        account = get_object_or_404(queryset)
        serializer = AccountSerializer(account)
        return Response(serializer.data)


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

