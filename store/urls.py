from django.urls import path

from .views import (
    product_list,
    product_detail,
    add_to_cart,
    cart,
    increase_quantity,
    decrease_quantity,
    remove_from_cart,
    checkout,
    signup,
    user_login,
    user_logout,
    order_history,
)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
      path('admin/', admin.site.urls),

    path('', product_list, name='product_list'),

    path('product/<int:id>/', product_detail, name='product_detail'),

    path('add-to-cart/<int:id>/', add_to_cart, name='add_to_cart'),

    path('cart/', cart, name='cart'),

    path('cart/increase/<int:id>/', increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:id>/', decrease_quantity, name='decrease_quantity'),
    path('cart/remove/<int:id>/', remove_from_cart, name='remove_from_cart'),

    path('checkout/', checkout, name='checkout'),

    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('orders/', order_history, name='orders'),

]