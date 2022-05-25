from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Prefetch, F, Sum
from geopy.distance import distance

from phonenumber_field.modelfields import PhoneNumberField

from distances.models import Place
from distances.yandex_api import fetch_coordinates


class RestaurantsQuerySet(models.QuerySet):
    def available_product_restaurants(self):
        prefetched_restaurants = self.prefetch_related(Prefetch(
            'menu_restaurants', queryset=RestaurantMenuItem.objects.select_related('product'))
        )
        return prefetched_restaurants.filter(menu_restaurants__availability=True).distinct()


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50,
        db_index=True,
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    objects = RestaurantsQuerySet.as_manager()

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
                .filter(availability=True)
                .values_list('product')
        )
        return self.filter(pk__in=products)


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=200,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_restaurants',
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_products',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"


class ProductInOrder(models.Model):
    product = models.ForeignKey(
        'Product', verbose_name='Продукт', related_name='products', on_delete=models.CASCADE)
    order = models.ForeignKey(
        'Order', verbose_name='Заказ', related_name='products_in_order', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('Количество', validators=[MinValueValidator(1), ])
    price = models.DecimalField('Цена продукта', max_digits=100, decimal_places=2, validators=[MinValueValidator(0), ],
                                help_text='Цена заполняется автоматически')

    class Meta:
        verbose_name = 'продукт заказа'
        verbose_name_plural = 'продукт заказов'

    def __str__(self):
        return f'{self.product.name} {self.quantity} {self.order}'


class OrderQuerySet(models.QuerySet):
    def not_processed(self):
        return self.filter(
            state=Order.OrderState.NOT_PROCESSED)

    def prefetch_available_restaurants(self):
        restaurants = Restaurant.objects.available_product_restaurants()

        orders = self.not_processed().prefetch_related(
            Prefetch('products_in_order', queryset=ProductInOrder.objects.select_related('product'))).annotate(
            order_price=(Sum(F('products_in_order__price') * F('products_in_order__quantity')))
        ).select_related('who_cook')
        addresses = list(restaurants.values_list('address', flat=True))
        addresses.extend(list(orders.values_list('address', flat=True)))

        places = {
            place.address: (place.lat, place.lon) if place.lat and place.lon else None
            for place in Place.objects.filter(address__in=addresses)
        }
        places_to_create = []

        for order in orders:
            if order.who_cook:
                continue

            if order.address in places:
                order_coordinates = places[order.address]
            else:
                order_coordinates = fetch_coordinates(settings.YANDEX_API_KEY, order.address)
                lat, lon = order_coordinates if order_coordinates else (None, None)
                places_to_create.append(Place(address=order.address, lat=lat, lon=lon))
            products_in_order = order.products_in_order.all()
            product_pks = [product_in_order.product.pk for product_in_order in products_in_order]
            order.available_restaurants = list()
            for restaurant in restaurants:
                restaurant_menu = restaurant.menu_restaurants.all()
                available_product_pks = [restaurant_menu.product.pk for restaurant_menu in restaurant_menu]
                for product_pk in product_pks:
                    if product_pk not in available_product_pks:
                        break
                else:
                    restaurant_address = restaurant.address
                    if restaurant_address in places:
                        restaurant_coordinates = places[restaurant_address]
                    else:
                        restaurant_coordinates = fetch_coordinates(settings.YANDEX_API_KEY, restaurant_address)
                        lat, lon = restaurant_coordinates if restaurant_coordinates else (None, None)
                        places_to_create.append(Place(address=restaurant_address, lat=lat, lon=lon))
                    if order_coordinates and restaurant_coordinates:
                        distance_km = distance(order_coordinates, restaurant_coordinates).km
                        repr_distance = f"{distance_km} км"
                    else:
                        distance_km = 0
                        repr_distance = 'ошибка определения координат'
                    serialized_restaurant = {
                        'distance_km': distance_km,
                        'repr_distance': repr_distance,
                        'address': restaurant_address,
                        'name': restaurant.name,
                    }
                    order.available_restaurants.append(serialized_restaurant)
            order.available_restaurants.sort(
                key=lambda serialized_restaurant: int(serialized_restaurant['distance_km']))
        Place.objects.bulk_create(places)
        return orders


class Order(models.Model):
    class OrderState(models.TextChoices):
        PROCESSED = 'PR', 'Обработанный'
        NOT_PROCESSED = 'NP', 'Необработанный'

    class PayMethodChoice(models.TextChoices):
        CASH = 'CS', 'Наличные'
        ELECTRONIC = 'EC', 'Электронный'
        NOT_CHOSEN = 'NC', 'Не выбрано'

    firstname = models.CharField(max_length=32, verbose_name='имя')
    lastname = models.CharField(max_length=64, verbose_name='фамилия')
    phonenumber = PhoneNumberField(verbose_name='номер телефона', db_index=True)
    address = models.CharField(max_length=256, verbose_name='адрес доставки')
    comment = models.TextField(verbose_name='Комментарий', blank=True)

    registered_at = models.DateTimeField(verbose_name='Дата регистрации заказа', auto_now=True, db_index=True)
    called_at = models.DateTimeField(verbose_name='Дата звонка', db_index=True, blank=True, null=True)
    delivered_at = models.DateTimeField(verbose_name='Дата доставки', db_index=True, blank=True, null=True)

    who_cook = models.ForeignKey(Restaurant, verbose_name='Кто готовит?', on_delete=models.SET_NULL,
                                 blank=True, null=True, related_name='order_who_cook'
                                 )

    state = models.CharField(
        max_length=2,
        choices=OrderState.choices,
        default=OrderState.NOT_PROCESSED,
        db_index=True,
        verbose_name='Статус заказа'
    )

    pay_method = models.CharField(
        max_length=2,
        choices=PayMethodChoice.choices,
        db_index=True,
        default=PayMethodChoice.NOT_CHOSEN,
        verbose_name='Способ оплаты',
    )

    objects = OrderQuerySet.as_manager()

    class Meta:
        verbose_name = 'заказ клиента'
        verbose_name_plural = 'заказы клиентов'

    def __str__(self):
        return f'{self.firstname} {self.address}'
