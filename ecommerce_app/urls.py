"""
URL configuration for ecommerce_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from core.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home),
    path('product/',product),
    path('create_account/',create_account),
    path('login/',login),
    path('user_home/',user_home),
    path('cart/',cart),
    path('add_to_cart/',add_to_cart, name='add_to_cart'),
    path('log_out/', log_out, name='log_out'),
    path('a_admin_home/',a_admin_home),
    path('a_product/',a_product),
    path('a_add_product/',a_add_product),
    path('a_edit_product/',a_edit_product),
    path('a_delete_product/',a_delete_product),
    path('product_det/',product_det),
    path('delete_from_cart/',delete_from_cart),
    path('checkout/',checkout),
    path('order/',order),
    path('a_users/',a_users),
    path('a_order_details/',a_order_details),
    path('order_details/',order_details)
]
