from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import ListField

from foodcartapp.models import Product, Order


class ProductsListSerializer(serializers.Serializer):
    product = serializers.IntegerField(min_value=0)
    quantity = serializers.IntegerField(min_value=1)

    def validate_product(self, value):
        try:
            Product.objects.get(pk=value)
        except Product.DoesNotExist:
            raise ValidationError(f'Не найден продукт с таким индикатором - {value}')
        return value


class OrderSerializer(serializers.ModelSerializer):
    products = ListField(
        child=ProductsListSerializer(), allow_empty=False,
    )

    class Meta:
        model = Order
        fields = ['firstname', 'lastname', 'phonenumber', 'address', 'products']
