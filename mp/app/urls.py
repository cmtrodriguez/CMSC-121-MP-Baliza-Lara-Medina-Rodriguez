from django.urls import path
from . import views


urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('buyer/', views.buyer_home, name='buyer'),
    path('seller/', views.seller_home, name='seller_home'),
    path('rolepage/', views.role_page, name='role_page'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout_page, name='checkout_page'),
    path('logout/', views.logout_view, name='logout'),

    # Product management URLs
    path('product/add/', views.add_product, name='add_product'),
    path('product/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('product/<int:product_id>/delete/', views.delete_product, name='delete_product'),

    # Cart-related URLs
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:product_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),

    path('sales/', views.seller_sales, name='seller_sales'),
]
