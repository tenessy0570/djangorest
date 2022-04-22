from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status

from .models import CustomUser, Product, ProductInCart, Order, OrderItem
from .serializers import ProductEditSerializer


def create_new_user_and_get_token(serialized_data):
    """Creates new user and returns its token"""
    full_name = serialized_data['full_name']
    username = serialized_data['email']
    password = serialized_data['password']
    email = serialized_data['email']
    new_user = CustomUser.objects.create_user(
        full_name=full_name,
        username=username,
        password=password,
        email=email
    )
    user_token = Token.objects.create(user=new_user).key
    return user_token


def get_response_422_with_errors(serialized):
    response = dict(
        code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        warning='Validation error',
        errors={
            **serialized.errors
        }
    )
    return Response(response, status=response['code'])


def get_response_201_with_token(token):
    return Response({'token': token}, status=status.HTTP_201_CREATED)


def get_response_404_not_found():
    response = dict(
        code=404,
        warning='Not found'
    )
    return Response(response, status.HTTP_404_NOT_FOUND)


def get_response_400_already_registered():
    return Response({"error": "Already registered"}, status=status.HTTP_400_BAD_REQUEST)


def get_response_403_message(message: str):
    response = dict(
        code=status.HTTP_403_FORBIDDEN,
        warning=message
    )
    return Response(response, status=status.HTTP_403_FORBIDDEN)


def get_response_200_with_message(message: str) -> Response:
    response = dict(
        message=message
    )
    return Response(response, status=status.HTTP_200_OK)


def get_response_201_product_added():
    response = dict(
        message='Product added to cart'
    )
    return Response(response, status=status.HTTP_201_CREATED)


def get_response_422_message(message: str):
    response = dict(
        code=422,
        message=message
    )
    return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


def get_response_201_order_submitted(order_id):
    response = dict(
        order_id=order_id,
        message='Order is processed'
    )
    return Response(response, status=status.HTTP_201_CREATED)


def get_user_token(user: object = None, email=None, return_object: bool = False):
    """Returns user token if exists. Else returns None"""
    if email:
        try:
            user = CustomUser.objects.get(username=email)
        except ObjectDoesNotExist:
            return None
        return get_user_token(user=user)
    if return_object:
        return Token.objects.get(user=user.pk)
    return Token.objects.get(user=user.pk).key


def generate_and_get_user_token(email: str = None, user: object = None):
    """Generates new token for user and returns it"""
    if email:
        user = CustomUser.objects.get(username=email)
    try:
        old_token = get_user_token(user=user, return_object=True)
    except ObjectDoesNotExist:
        pass
    else:
        old_token.delete()
    finally:
        generated_token = Token.objects.create(user=user).key
    return generated_token


def get_user_by_its_token(token: str):
    """
    Takes token as argument. If user with this token exists,
    returns it. If not - returns None
    """
    try:
        user = Token.objects.get(key=token).user
    except ObjectDoesNotExist:
        return None
    return user


def get_token_from_request(request):
    """
    Returns bearer token from request if exists,
    else returns None
    """
    try:
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[-1]
    except:
        return None
    return token


def get_email_and_password_from_request(request):
    email = request.data['email']
    password = request.data['password']
    return email, password


def user_is_authenticated_with_token(request):
    """Returns True if user is authenticated with token, else returns False"""
    request_token = get_token_from_request(request=request)
    if request_token:
        try:
            Token.objects.get(key=request_token)
        except Exception:
            return False
        return True
    return False


def check_if_user_already_registered(request):
    if user_is_authenticated_with_token(request):
        return get_response_400_already_registered()
    return False


def check_email_and_password(email, password):
    """Returns True if email and password match is valid, if not - returns False"""
    try:
        user = CustomUser.objects.get(username=email)
    except ObjectDoesNotExist:
        return False

    user_password = user.password
    return check_password(password, user_password)


def get_user_object_from_request(request):
    """Returns object 'user' based on token in request"""
    request_token = get_token_from_request(request=request)
    request_user = get_user_by_its_token(request_token)
    return request_user


def add_product_to_user_cart(user, product_id):
    """Adds specific product to user's cart"""
    product = get_product_by_its_id(product_id=product_id)
    if product:
        user_cart = user.cart
        ProductInCart.objects.create(user_cart=user_cart, cart_product=product)
        return True
    return False


def success_added_product_response(success: bool):
    if success:
        return get_response_201_product_added()
    return get_response_404_not_found()


def success_deleted_item_from_cart_response(success: bool):
    if success:
        return get_response_200_with_message(message='Item removed from cart')
    return get_response_404_not_found()


def get_product_by_its_id(product_id):
    """Returns product if exists. Else - None"""
    try:
        product = Product.objects.get(pk=product_id)
    except ObjectDoesNotExist:
        return None
    return product


def get_user_cart_items(user: object):
    """Returns user's cart items"""
    try:
        cart_items = ProductInCart.objects.filter(user_cart=user.cart.pk)
    except Exception:
        return None
    return cart_items


def get_response_with_cart_items(cart_items):
    """Generates response with cart items"""
    response = dict(items=[])
    for item in cart_items:
        item_product = item.cart_product
        response['items'].append(dict(
            id=item.id,
            product_id=item_product.id,
            name=item_product.name,
            info=item_product.info,
            price=item_product.price
        ))
    return response


def get_response_200_with_cart_list(user: object):
    """Returns products list from user's cart"""
    cart_items = get_user_cart_items(user=user)
    response = get_response_with_cart_items(cart_items=cart_items)
    return Response(response, status=status.HTTP_200_OK)


def delete_cart_item(request, item_id: int):
    """Deletes item from user's cart"""
    user = get_user_object_from_request(request)
    user_cart = user.cart.pk
    try:
        cart_item = ProductInCart.objects.get(user_cart=user_cart, id=item_id)
    except ObjectDoesNotExist:
        return False
    cart_item.delete()
    return True


def user_logout(request) -> None:
    token = get_token_from_request(request)
    user = get_user_by_its_token(token)
    token_instance = Token.objects.get(user=user.pk, key=token)
    token_instance.delete()


def order_submit_and_get_id(request):
    user = get_user_object_from_request(request)
    user_cart_items = get_user_cart_items(user)
    if user_cart_items.count() == 0:
        raise IndexError
    order = Order.objects.create(client=user)
    for item in user_cart_items:
        order_item = OrderItem.objects.create(item=item.cart_product, user_order=order)
        order.items.add(order_item)
    order.save()
    user_cart = user.cart
    ProductInCart.objects.filter(user_cart=user_cart.pk).delete()
    return order.pk


def get_user_orders_list(request):
    user = get_user_object_from_request(request)
    user_orders, price_all = get_user_orders_and_price(user=user)
    return user_orders, price_all


def get_user_orders_and_price(user):
    orders = Order.objects.filter(client=user.pk)
    price_all = 0
    orders_list = []
    for order in orders:
        order_price = 0
        order_items = order.items.all()
        order_items_only_id = [item.item.pk for item in order_items]

        for order_item in order_items:
            order_price += order_item.item.price

        orders_list.append(dict(
            id=order.pk,
            products=order_items_only_id,
            order_price=order_price
        ))
        price_all += order_price
    return orders_list, price_all


def get_response_200_with_orders_list(user_orders, price_all):
    response = dict(
        items=user_orders,
        price_all=price_all
    )
    return Response(response, status=status.HTTP_200_OK)


def user_is_staff(request):
    user = get_user_object_from_request(request)
    if not user:
        return False
    return user.is_staff


def delete_product(product_id):
    product = get_product_by_its_id(product_id)
    if not product:
        raise ObjectDoesNotExist
    product.delete()


def create_new_product_and_get_id(data):
    new_product = Product.objects.create(
        name=data['name'],
        info=data['info'],
        price=data['price']
    )
    return new_product.pk


def get_response_201_product_created(new_product_id):
    response = dict(
        id=new_product_id,
        message='Service added'
    )
    return Response(response, status=status.HTTP_201_CREATED)


def update_and_get_product(data, product_id):
    product = get_product_by_its_id(product_id)
    serialized = ProductEditSerializer(product, data=data)

    if serialized.is_valid():
        serialized.save()

    return product


def get_response_200_product_editted_successfully(product):
    response = dict(
        items=dict(
            id=product.id,
            name=product.name,
            info=product.info,
            price=product.price
        )
    )
    return Response(response, status=status.HTTP_200_OK)
