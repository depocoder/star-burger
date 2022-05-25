from django.db import transaction
from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response

from foodcartapp.models import Product, Order, ProductInOrder
from .serializer import OrderSerializer


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            },
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@api_view(['POST'])
@transaction.atomic
def register_order(request):
    serializer = OrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    loaded_order = serializer.data
    order = Order.objects.create(
        firstname=loaded_order['firstname'],
        lastname=loaded_order['lastname'],
        phonenumber=loaded_order['phonenumber'],
        address=loaded_order['address']
    )
    products_in_order_to_create = []
    products = {product['product']: product['quantity'] for product in loaded_order['products']}
    for product in Product.objects.filter(pk__in=products.keys()):
        products_in_order_to_create.append(ProductInOrder(
            order=order,
            product=product,
            quantity=products[product.pk],
            price=product.price,
        ))
    ProductInOrder.objects.bulk_create(products_in_order_to_create)
    return Response(loaded_order)
