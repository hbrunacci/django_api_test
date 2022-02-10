from django.db import models

# Create your models here.


class Product(models.Model):
    id = models.CharField(primary_key=True, max_length=12, unique=True, null=False, blank=False)
    name = models.CharField(max_length=100, null=False, blank=False)
    price = models.FloatField(null=False)
    stock = models.IntegerField(null=False, default=0)

    def __str__(self):
        return self.name

    def add_stock(self, quantity):
        self.stock += quantity
        self.save()
        return True

    def substract_stock(self, quantity=0):
        if self.stock - quantity >= 0:
            self.stock -= quantity
            self.save()
            return True
        else:
            return False
