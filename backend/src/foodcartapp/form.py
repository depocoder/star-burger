from django import forms

from foodcartapp.models import Restaurant


class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        restaurants_with_complete_set = Restaurant.objects.get_restaurants_with_order_products(self.instance.pk)
        restaurant_with_complete_set_pks = [restaurant.pk for restaurant in restaurants_with_complete_set]
        self.fields['who_cook'].queryset = Restaurant.objects.filter(id__in=restaurant_with_complete_set_pks)
