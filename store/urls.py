from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name="home"),
    path('store/',views.store, name="store"),
    path('register/', views.registerPage, name="register"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('products/', views.products, name="products"),
    path('customer/<str:pk>/', views.customer, name="customer"),
    path('product/<int:product_id>/', views.detail, name="detail"),
    path('search/', views.search, name="search"),
    path('create_order/<str:pk>/', views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),
    path('update_order1/<str:pk>/', views.updateOrder1, name="update_order1"),
    path('delete_order1/<int:order_id>/<int:order_item_id>/', views.deleteOrder1, name="delete_order1"),
    path('user/', views.UserPage, name="user-page"),
    path('ripota/', views.ripota, name="ripota"),
    path('generate_pdf_report/', views.generate_pdf_report, name='customer_report'),
    path('ripota1/', views.ripota1, name="ripota1"),
    path('accesstoken/', views.get_access_token, name="get_access_token"),
    path('stkpush/', views.initiate_stk_push, name="initiate_stk_push"),
    path('query/', views.query_stk_status, name="query_stk_status"),
    path('index/', views.index, name="index"),

] 