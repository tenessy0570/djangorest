from django.contrib.auth import get_user_model
from rest_framework import serializers

from app.models import CustomUser, Product, Cart
from app.validators import validate_password

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            full_name=validated_data['full_name'],
            username=validated_data['email'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        return user

    @staticmethod
    def validate_password(data):
        validate_password(data=data)

    class Meta:
        model = CustomUser
        fields = ('full_name', 'email', 'password')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'info', 'price')


class ProductEditSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255, required=False, allow_blank=False)
    info = serializers.CharField(max_length=1000, required=False, allow_blank=False)
    price = serializers.IntegerField(required=False)

    class Meta:
        model = Product
        fields = ('name', 'info', 'price')


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('products',)
