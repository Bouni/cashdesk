from django.db import models

class Item(models.Model):

    brand = models.CharField(max_length=120)
    name = models.CharField(max_length=120)
    price = models.DecimalField(decimal_places=2, max_digits=6, default=0)
    image = models.CharField(max_length=1024, unique=True, null=True, blank=True)
    size = models.CharField(max_length=120, null=True, blank=True)
    stock = models.BooleanField(default=True)
    category = models.ForeignKey(
        "ItemCategory",
        on_delete=models.DO_NOTHING,
        related_name="category",
        related_query_name="category",
        null=True
    )

    class Meta:
        ordering = ['-stock']
        constraints = [models.UniqueConstraint(fields=['brand', 'name'], name='unique item')]

    def __str__(self):
        return f"{self.brand} {self.name}"


class ItemCategory(models.Model):

    name = models.CharField(max_length=120, unique=True)
    
    def __str__(self):
        return self.name
