from rest_framework import serializers
from .models import Order, OrderDetail
from django.utils.translation import gettext as _

class OrderDetailModelSeliarizer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=False, required=False)

    class Meta:
        model = OrderDetail
        fields = (
            'id',
            'order',
            'quantity',
            'product',
        )
        read_only_fields = ("order",)


    def validate_quantity(self, value):
        if value < 1 :
            raise serializers.ValidationError('La cantidad no puede ser menor a 1')
        return value

class OrderModelSerializer(serializers.ModelSerializer):

    items = OrderDetailModelSeliarizer(many=True)

    class Meta:
        model = Order
        fields = (
            'id',
            'date_time',
            'get_total',
            'get_total_usd',
            'items',
        )
        read_only_fields = (
            'get_total',
            'get_total_usd',)

    def create(self, validated_data):
        order_items = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item in order_items:
            OrderDetail.objects.create(order=order, **item)
        return order


    def update(self, instance, validated_data):
        new_data = {item_data.get('product').id: item_data.get('quantity') for item_data in validated_data.get('items')}

        for item in instance.items.all():
            new_value = new_data.get(item.product.id, 0)
            if new_value and not item.can_update(new_value):
                raise serializers.ValidationError(_('Sin stok suficiente'))

        for item in instance.items.all():
            new_value = new_data.get(item.product.id, 0)
            if new_value > 0:
                item.quantity = new_value
                item.save()
            elif new_value == 0 and not self.partial:
                item.delete()


        instance.save()
        return instance