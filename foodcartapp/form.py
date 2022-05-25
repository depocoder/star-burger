from django import forms

from foodcartapp.models import Restaurant


class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['who_cook'].queryset = Restaurant.objects.get_restaurants_with_order_products(self.instance.pk)
