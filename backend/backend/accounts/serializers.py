from django.db import models
from rest_framework import serializers

from .models import Account, Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"


class AccountSerializer(serializers.ModelSerializer):

    balance = serializers.ReadOnlyField()
    transaction = TransactionSerializer(many=True, read_only=True)

    class Meta:
        model = Account
        fields = "__all__"


