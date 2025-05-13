from django.urls import path
from . import views


urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('buyer/', views.buyer_home, name='buyer'),
    path('seller/', views.seller_home, name='seller_home'),
    path('rolepage/', views.role_page, name='role_page'),
    path('cart/', views.cart_page, name='cart_page'),
    path('checkout/', views.checkout_page, name='checkout_page'),
    

]
