from django.urls import path
from django.shortcuts import redirect

from . import views

app_name = "restaurateurapp"

urlpatterns = [
    path('', lambda request: redirect('restaurateurapp:ProductsView')),

    path('products/', views.view_products, name="ProductsView"),

    path('restaurants/', views.view_restaurants, name="RestaurantView"),

    path('orders/', views.view_orders, name="view_orders"),

    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
]
