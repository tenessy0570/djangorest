from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from rest_framework.authtoken.models import Token


class CustomUser(AbstractUser):
    email = models.EmailField(max_length=255, null=False, blank=False, unique=True)
    full_name = models.CharField(max_length=255, null=False, blank=False)
    username = models.CharField(max_length=255, null=True, default=None, unique=True)
    password = models.CharField(max_length=255, null=False, blank=False, unique=True)
    cart = models.OneToOneField('Cart', on_delete=models.CASCADE, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'password')

    def save(self, *args, **kwargs):
        if not self.pk:
            self.cart = Cart.objects.create()
        super().save()

    def get_token(self):
        return Token.objects.get(user=self.pk)


class Product(models.Model):
    """Продукт"""
    name = models.CharField(max_length=255, null=False, blank=False)
    info = models.TextField(null=False, blank=False)
    price = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return self.name


class Cart(models.Model):
    """Корзина клиента"""
    products = models.ManyToManyField('ProductInCart')

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'


class ProductInCart(models.Model):
    """Список продуктов в корзине клиента"""
    user_cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    cart_product = models.ForeignKey('Product', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'cart item'


class Order(models.Model):
    """Заказ"""
    client = models.ForeignKey('CustomUser', on_delete=models.CASCADE, null=False)
    items = models.ManyToManyField('OrderItem')


class OrderItem(models.Model):
    """Список продуктов внутри заказа"""
    item = models.ForeignKey('Product', on_delete=models.CASCADE, null=False)
    user_order = models.ForeignKey('Order', on_delete=models.CASCADE, null=False)
