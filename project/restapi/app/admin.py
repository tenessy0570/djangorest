from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Product, Cart, ProductInCart, Order, OrderItem


class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'full_name', 'cart')


class CartItem(admin.ModelAdmin):
    list_display = ('id', 'user_cart', 'cart_product')


class CartAdmin(admin.ModelAdmin):
    list_display = ('id',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Product)
admin.site.register(Cart, CartAdmin)
admin.site.register(ProductInCart, CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)