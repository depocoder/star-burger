from django import forms
from django.contrib.auth.views import LoginView

from foodcartapp.models import Restaurant


class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # order = self.instance
        # self.fields[
        #     'restaurant'
        # ].queryset = Restaurant.objects(order.id)