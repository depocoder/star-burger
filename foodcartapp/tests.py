import json
import os
from pathlib import Path

from foodcartapp.models import Product, ProductCategory, Restaurant

from django.contrib.auth.models import User
from rest_framework.test import APITransactionTestCase





class TestRegisterOrder(APITransactionTestCase):
    endpoint = '/api/order/'
    is_logined = False

    @staticmethod
    def create_user():
        return User.objects.create_superuser(
            username='test',
            email='test@test',
            password='test',
            first_name='test',
            last_name='test'
        )

    @staticmethod
    def create_products():
        fixture_path = Path(os.getcwd(), 'foodcartapp/fixture/products.json')
        with open(fixture_path) as products_file:
            products = json.load(products_file)
        for product in products:
            product_category = product.pop('category')
            product['category'], _ = ProductCategory.objects.get_or_create(name=product_category)
            product['image'] = 'fixture/beconizer.jpg'
            Product.objects.create(**product)

    @staticmethod
    def create_restaurants():
        fixture_path = Path(os.getcwd(), 'foodcartapp/fixture/restautants.json')
        with open(fixture_path) as restaurants_file:
            restaurants = json.load(restaurants_file)
        for restaurant in restaurants:
            Restaurant.objects.create(**restaurant)

    def setUp(self):
        self.create_products()
        self.create_restaurants()
        if not self.is_logined:
            self.create_user()
            self.client.login(
                username='test',
                password='test',
            )

            self.is_logined = True

    def test_create(self):
        product = Product.objects.first()
        order = {
            "products": [{"product": product.pk, "quantity": 3}],
            "firstname": "Тимур",
            "lastname": "Иванов",
            "phonenumber": "+7 901 999 99 99",
            "address": "Москва, улица Охотный Ряд, 2"
        }
        response = self.client.post(
            self.endpoint,
            data=order,
            format='json',

        )
        assert response.status_code == 200
        results = response.json()
        assert results
        assert results['products'] == order['products']
        assert results['firstname'] == order['firstname']
        assert results['phonenumber'] == order['phonenumber']
        assert results['address'] == order['address']

    def test_error_products_is_str(self):
        """Продукты — это не список, а строка."""
        error = 'Ожидался list со значениями, но был получен "str".'
        order = {"products": "HelloWorld", "firstname": "Иван", "lastname": "Петров", "phonenumber": "+79291000000",
                 "address": "Москва"}
        response = self.client.post(
            self.endpoint,
            data=order,
            format='json',

        )
        assert response.status_code == 400
        results = response.json()
        assert error in results['products']

    def test_error_products_is_null(self):
        """Продукты — это null."""
        error = 'Это поле не может быть пустым.'
        order = {"products": None, "firstname": "Иван", "lastname": "Петров", "phonenumber": "+79291000000",
                 "address": "Москва"}
        response = self.client.post(
            self.endpoint,
            data=order,
            format='json',

        )
        assert response.status_code == 400
        results = response.json()
        assert error in results['products']

    def test_error_products_is_empty(self):
        """Продукты — пустой список."""
        error = 'Этот список не может быть пустым.'
        order = {"products": [], "firstname": "Иван", "lastname": "Петров", "phonenumber": "+79291000000",
                 "address": "Москва"}
        response = self.client.post(
            self.endpoint,
            data=order,
            format='json',

        )
        assert response.status_code == 400
        results = response.json()
        assert error in results['products']

    def test_error_do_not_have_products(self):
        """Продуктов нет."""
        error = 'Обязательное поле.'
        order = {"firstname": "Иван", "lastname": "Петров", "phonenumber": "+79291000000", "address": "Москва"}
        response = self.client.post(
            self.endpoint,
            data=order,
            format='json',

        )
        assert response.status_code == 400
        results = response.json()
        assert error in results['products']

    def test_error_firstname_is_empty(self):
        """firstname: Это поле не может быть пустым."""
        error = 'Это поле не может быть пустым.'
        order = {"products": [{"product": 1, "quantity": 1}], "firstname": None, "lastname": "Петров",
                 "phonenumber": "+79291000000", "address": "Москва"}
        response = self.client.post(
            self.endpoint,
            data=order,
            format='json',

        )
        assert response.status_code == 400
        results = response.json()
        assert error in results['firstname']

    def test_error_do_not_have_order_keys(self):
        """
        Ключей заказа вообще нет.
        firstname, lastname, phonenumber, address: Обязательное поле.
        """
        product = Product.objects.first()
        error = 'Обязательное поле.'
        order = {"products": [{"product": product.pk, "quantity": 1}]}
        response = self.client.post(
            self.endpoint,
            data=order,
            format='json',

        )
        assert response.status_code == 400
        results = response.json()
        assert error in results['firstname']
        assert error in results['lastname']
        assert error in results['phonenumber']
        assert error in results['address']

    def test_error_missing_phone_number(self):
        """Номер телефона пустая строка"""
        error = 'Это поле не может быть пустым.'
        product = Product.objects.first()
        order = {"products": [{"product": product.pk, "quantity": 1}], "firstname": "Тимур", "lastname": "Иванов",
                 "phonenumber": "", "address": "Москва, Новый Арбат 10"}
        response = self.client.post(
            self.endpoint,
            data=order,
            format='json',

        )
        assert response.status_code == 400
        results = response.json()
        assert error in results['phonenumber']

    def test_error_not_valid_phone_numer(self):
        """Несуществующий номер телефона."""
        error = 'Введен некорректный номер телефона.'
        product = Product.objects.first()
        order = {"products": [{"product": product.pk, "quantity": 1}], "firstname": "Тимур", "lastname": "Иванов",
                 "phonenumber": "+70000000000", "address": "Москва, Новый Арбат 10"}
        response = self.client.post(
            self.endpoint,
            data=order,
            format='json',

        )
        assert response.status_code == 400
        results = response.json()
        assert error in results['phonenumber']

    def test_error_not_existing_product(self):
        """Заказ с неуществующим id продукта."""
        product_id = 1_000_000
        error = f'Не найден продукт с таким индикатором - {product_id}'
        order = {"products": [{"product": product_id, "quantity": 1}], "firstname": "Иван", "lastname": "Петров",
                 "phonenumber": "+79291000000", "address": "Москва"}
        response = self.client.post(
            self.endpoint,
            data=order,
            format='json',

        )
        assert response.status_code == 400
        results = response.json()
        assert error in results['products']['0']['product']

    def test_error_firstname_is_str(self):
        """В поле firstname положили список."""
        product = Product.objects.first()
        error = {'firstname': ['Not a valid string.']}

        order = {"products": [{"product": product.pk, "quantity": 1}], "firstname": [], "lastname": "Петров",
                 "phonenumber": "+79291000000", "address": "Москва"}
        response = self.client.post(
            self.endpoint,
            data=order,
            format='json',
        )
        assert response.status_code == 400
        results = response.json()
        assert error == results
