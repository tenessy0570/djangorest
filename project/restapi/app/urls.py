from django.urls import path

from . import views

urlpatterns = [
    path('register', views.RegisterView.as_view(), name='register'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('products', views.ProductListAPIView.as_view(), name='products_list'),
    path('cart', views.CartListView.as_view(), name='cart_list'),
    path('cart/<int:item_id>', views.DeleteOrAddToCartView.as_view(), name='add_or_delete_from_cart'),
    path('order', views.OrdersGetOrSubmitView.as_view(), name='orders'),
    path('service/', views.ProductCreateView.as_view(), name='product_create'),
    path('service/<int:product_id>', views.ProductDeleteOrEditView.as_view(), name='product_edit')
]

