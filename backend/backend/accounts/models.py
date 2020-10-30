from django.db import models


class Transaction(models.Model):

    timestamp = models.DateTimeField(auto_now_add=True)
    value = models.DecimalField(decimal_places=2, max_digits=6, default=0)
    comment = models.CharField("comment", max_length=256)
    type = models.CharField("type", max_length=24)
    revoked = models.BooleanField(default=False)
    account = models.ForeignKey(
        "Account",
        on_delete=models.DO_NOTHING,
        related_name="transaction",
        related_query_name="transaction",
    )

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ("-timestamp",)

    def __str__(self):
        return f"Transaction #{self.id}"


class Account(models.Model):

    owner = models.CharField(max_length=120, unique=True)
    email = models.CharField(max_length=120, unique=True)
    matrix = models.CharField(max_length=120, unique=True)

    @property
    def balance(self):
        v = self.transaction.all()
        return (
            self.transaction.filter(revoked=False)
            .aggregate(models.Sum("value"))
            .get("value__sum", 0.00)
            or 0.00
        )

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"
        ordering = ("owner",)

    def __str__(self):
        return f"{self.owner}'s Account"
