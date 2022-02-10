from rest_framework import serializers
from .models import Product

class ProductModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'price',
            'stock'
        )

#
# class ProductSerializer(serializers.Serializer):
#     id = serializers.CharField(allow_null=False, max_length=12, required=True)
#     name = serializers.CharField(allow_null=False, max_length=50, required=True)
#     price = serializers.FloatField(required=True)
#     stock = serializers.IntegerField(default=0)
#
#     def create(self, validated_data):
#         product = Product.objects.create(**validated_data)
#         return product

