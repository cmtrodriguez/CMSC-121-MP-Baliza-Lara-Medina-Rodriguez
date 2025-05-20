from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Product, Order, CartItem

<<<<<<< HEAD
# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Product, Order, CartItem

=======
>>>>>>> ef4a8409a53c2a24ca735d0f2e30ade2e55634b9
# Register Product model
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'seller', 'created_at')
    list_filter = ('category', 'seller', 'created_at')
    search_fields = ('name', 'seller__username')
    ordering = ('-created_at',)

# Register Order model
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('product', 'buyer', 'quantity', 'total_price', 'purchased_at', 'payment_method')
    list_filter = ('purchased_at', 'payment_method', 'buyer')
    search_fields = ('product__name', 'buyer__username')
    ordering = ('-purchased_at',)

# Register CartItem model
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'added_at')
    list_filter = ('added_at', 'user')
    search_fields = ('user__username', 'product__name')
    ordering = ('-added_at',)

# Customize User admin
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)

# Unregister the default UserAdmin and register our custom one
admin.site.unregister(User)
<<<<<<< HEAD
admin.site.register(User, CustomUserAdmin)
=======
admin.site.register(User, CustomUserAdmin)
>>>>>>> ef4a8409a53c2a24ca735d0f2e30ade2e55634b9
