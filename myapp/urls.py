from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,  name='home-page'),
    path('registration', views.userReg, name='reg-page'),
    path('login', views.userLogin, name='log-page'),
    path('logout', views.userLogout, name='logout-page'),
    path('addtocart/<int:id>', views.add_to_cart, name='addtocart'),
    path('cart', views.view_cart, name='crt-page'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/delete/<int:item_id>/', views.delete_cart_item, name='delete_cart_item'),
    path('initiate-payment/', views.initiate_payment, name='initiate_payment'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path("my-orders", views.my_orders, name="my_orders"),
    path('shop', views.shop, name='shop-page'),
    path('shop/<int:id>', views.shopCat, name='shop-cat-page'),
    path('contact', views.contact, name='cont-page')
]