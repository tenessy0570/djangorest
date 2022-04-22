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
    """
    Product
    """
    name = models.CharField(max_length=255, null=False, blank=False)
    info = models.TextField(null=False, blank=False)
    price = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return self.name


class Cart(models.Model):
    """
    Client's cart
    """
    products = models.ManyToManyField('ProductInCart')

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'


class ProductInCart(models.Model):
    """
    A product that is inside of user's cart
    """
    user_cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    cart_product = models.ForeignKey('Product', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'cart item'


class Order(models.Model):
    """
    User's order (which contains products)
    """
    client = models.ForeignKey('CustomUser', on_delete=models.CASCADE, null=False)
    items = models.ManyToManyField('OrderItem')


class OrderItem(models.Model):
    """
    A product that is inside user's order
    """
    item = models.ForeignKey('Product', on_delete=models.CASCADE, null=False)
    user_order = models.ForeignKey('Order', on_delete=models.CASCADE, null=False)
