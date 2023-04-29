from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('',home,name="home"),
    path('signup/',signUp,name="signup"),
    path('login/',loginuser,name="log_in"),
    path('logout/',logoutuser,name="logout"),
    path('store/',storeProducts,name="store_products"),
    path('cart/',cart,name="cart_content"),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/increase/<int:product_id>/',increase_quantity,name='increase_quantity'),
    path('cart/decrease/<int:product_id>/', decrease_quantity, name='decrease_quantity'),
    path('store/category/<int:category_id>/',get_categories,name='get_by_category'),
    path('checkout/',checkout,name='checkout'),
    path('<slug:slug>/', product_detail, name='product_detail'),
]