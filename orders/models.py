from django.db import models
from .functions import get_dolar_price_today
from django.utils import timezone
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError
# Create your models here.


class Order(models.Model):
    date_time = models.DateTimeField(default=timezone.now, null=False, blank=False)

    @property
    def get_total(self):
        return sum([item.quantity * item.product.price for item in self.items.all()])

    @property
    def get_total_usd(self):
        dolar_price = get_dolar_price_today()
        total = self.get_total
        return round(total / dolar_price, 2) if dolar_price > 0 else 0

    def delete(self, using=None, keep_parents=False):
        for item in self.items.all():
            item.delete()
        super(Order, self).delete()


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    #En el doc decia cuantity, supongo será un Typo
    quantity = models.IntegerField(blank=False, null=False)
    product = models.ForeignKey('products.Product', on_delete=models.PROTECT)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['order', 'product'], name='unique_item')]


    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.id:
            old_value = OrderDetail.objects.get(id=self.id)
            if old_value.quantity > self.quantity:
                self.product.add_stock(old_value.quantity - self.quantity)
            elif old_value.quantity < self.quantity:
                if not self.product.substract_stock(self.quantity - old_value.quantity):
                    raise ValidationError(_('Sin stock suficiente'))
        else:
            if not self.product.substract_stock(self.quantity):
                raise ValidationError(_('Sin stock suficiente'))
        super(OrderDetail, self).save()

    def can_update(self, new_value=0):
        return (self.product.stock - self.quantity + new_value) > 0



    def get_as_dict_by_product(self):
        return {self.product_id: {'quantity': self.quantity, 'order': self.order, 'id': self.id}}


    def delete(self, using=None, keep_parents=False):
        self.product.add_stock(self.quantity)
        super(OrderDetail, self).delete()


