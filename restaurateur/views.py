from django import forms
from django.db.models import Prefetch, Sum, F
from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views

from django.conf import settings
from geopy.distance import distance

from foodcartapp.models import Product, Restaurant, Order, ProductInOrder
from distances.models import Place
from distances.yandex_api import fetch_coordinates


class Login(forms.Form):
    username = forms.CharField(
        label='Логин', max_length=75, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Укажите имя пользователя'
        })
    )
    password = forms.CharField(
        label='Пароль', max_length=75, required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = Login()
        return render(request, "login.html", context={
            'form': form
        })

    def post(self, request):
        form = Login(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.is_staff:  # FIXME replace with specific permission
                    return redirect("restaurateur:RestaurantView")
                return redirect("start_page")

        return render(request, "login.html", context={
            'form': form,
            'ivalid': True,
        })


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('restaurateur:login')


def is_manager(user):
    return user.is_staff  # FIXME replace with specific permission


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_products(request):
    restaurants = list(Restaurant.objects.order_by('name'))
    products = list(Product.objects.prefetch_related('menu_products'))

    default_availability = {restaurant.id: False for restaurant in restaurants}
    products_with_restaurants = []
    for product in products:
        availability = {
            **default_availability,
            **{item.restaurant_id: item.availability for item in product.menu_products.all()},
        }
        orderer_availability = [availability[restaurant.id] for restaurant in restaurants]

        products_with_restaurants.append(
            (product, orderer_availability)
        )

    return render(request, template_name="products_list.html", context={
        'products_with_restaurants': products_with_restaurants,
        'restaurants': restaurants,
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_restaurants(request):
    return render(request, template_name="restaurants_list.html", context={
        'restaurants': Restaurant.objects.all(),
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_orders(request):
    restaurants = Restaurant.objects.prefetch_products()

    orders = Order.objects.not_processed().prefetch_related(
        Prefetch('products_in_order', queryset=ProductInOrder.objects.select_related('product'))).annotate(
        order_price=(Sum(F('products_in_order__price') * F('products_in_order__quantity')))
    ).select_related('who_cook')

    addresses = list(restaurants.values_list('address', flat=True))
    addresses.extend(list(orders.values_list('address', flat=True)))
    places = {
        place.address: (place.lat, place.lon) for place in Place.objects.filter(address__in=addresses)
    }
    places_to_create = []

    for order in orders:
        products_in_order = order.products_in_order.all()
        order.available_restaurants = Restaurant.objects.get_restaurants_with_order_products(
            order.pk, restaurants, products_in_order
        )

    for order in orders:
        if order.who_cook:
            continue
        order.serialized_restaurants = []
        if order.address in places:
            order_coordinates = places[order.address]
        else:
            order_coordinates = fetch_coordinates(settings.YANDEX_API_KEY, order.address)
            lat, lon = order_coordinates
            places_to_create.append(Place(address=order.address, lat=lat, lon=lon))
            places[order.address] = order_coordinates
        for restaurant in order.available_restaurants:
            restaurant_address = restaurant.address
            if restaurant_address in places:
                restaurant_coordinates = places[restaurant_address]
            else:
                restaurant_coordinates = fetch_coordinates(settings.YANDEX_API_KEY, restaurant_address)
                lat, lon = restaurant_coordinates
                places[restaurant.address] = restaurant_coordinates
                places_to_create.append(Place(address=restaurant_address, lat=lat, lon=lon))
            if all(order_coordinates) and all(restaurant_coordinates):
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
            order.serialized_restaurants.append(serialized_restaurant)
        del order.available_restaurants
        order.serialized_restaurants.sort(
            key=lambda serialized_restaurant: int(serialized_restaurant['distance_km']))
    Place.objects.bulk_create(places_to_create)

    return render(request, template_name='order_items.html', context={
        'order_items': orders,
    })
