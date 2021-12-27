from .decorators import auth_required, is_staff_required
from .serializers import UserSerializer, ProductSerializer
from .utils import *
from rest_framework import generics
from rest_framework.views import APIView


class RegisterView(APIView):
    @staticmethod
    def post(request):
        serialized = UserSerializer(data=request.data)

        if serialized.is_valid():
            token = create_new_user_and_get_token(serialized_data=serialized.initial_data)
            return get_response_201_with_token(token)

        return get_response_422_with_errors(serialized)


class LoginView(APIView):
    @staticmethod
    def post(request):
        email, password = get_email_and_password_from_request(request=request)

        if check_email_and_password(email=email, password=password):
            token = generate_and_get_user_token(email=email)
            return get_response_201_with_token(token=token)

        return get_response_403_message(message='Login failed')


class ProductListAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all()


class DeleteOrAddToCartView(APIView):
    @staticmethod
    @auth_required
    def delete(request, item_id):
        success = delete_cart_item(request=request, item_id=item_id)
        return success_deleted_item_from_cart_response(success)

    @staticmethod
    @auth_required
    def post(request, item_id):
        request_user = get_user_object_from_request(request)
        success = add_product_to_user_cart(user=request_user, product_id=item_id)
        return success_added_product_response(success)


class CartListView(APIView):
    @staticmethod
    @auth_required
    def get(request):
        user = get_user_object_from_request(request)
        return get_response_200_with_cart_list(user=user)


class LogoutView(APIView):
    @staticmethod
    @auth_required
    def get(request):
        user_logout(request)
        return get_response_200_with_message(message='logout')


class OrdersGetOrSubmitView(APIView):
    @staticmethod
    @auth_required
    def post(request):
        try:
            order_id = order_submit_and_get_id(request)
        except IndexError:
            return get_response_422_message(message='Cart is empty')
        return get_response_201_order_submitted(order_id)

    @staticmethod
    @auth_required
    def get(request):
        user_orders, price_all = get_user_orders_list(request)
        return get_response_200_with_orders_list(user_orders, price_all)


class ProductDeleteOrEditView(APIView):
    @staticmethod
    @is_staff_required
    def delete(request, product_id):
        try:
            delete_product(product_id=product_id)
        except ObjectDoesNotExist:
            return get_response_404_not_found()
        return get_response_200_with_message(message='Service removed')

    @staticmethod
    @is_staff_required
    def patch(request, product_id):
        serialized = ProductEditSerializer(data=request.data)

        if serialized.is_valid():
            product = update_and_get_product(data=request.data, product_id=product_id)
            return get_response_200_product_editted_successfully(product)

        return get_response_422_with_errors(serialized)


class ProductCreateView(APIView):
    @staticmethod
    @is_staff_required
    def post(request):
        serialized = ProductSerializer(data=request.data)

        if serialized.is_valid():
            new_product_id = create_new_product_and_get_id(serialized.initial_data)
            return get_response_201_product_created(new_product_id)

        return get_response_422_with_errors(serialized)
