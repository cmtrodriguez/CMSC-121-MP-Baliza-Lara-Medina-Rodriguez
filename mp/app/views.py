from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ProductForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib.auth.models import Group

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('role_page')  # Redirect to role page after login
        else:
            return render(request, 'app/login.html', {'error': 'Invalid credentials'})
    return render(request, 'app/login.html')

# User Signup View
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='Buyer')  # Assign 'Buyer' role by default
            user.groups.add(group)
            login(request, user)
            return redirect('role_page')  # Redirect to the role selection page after signup
    else:
        form = UserCreationForm()
    return render(request, 'app/signup.html', {'form': form})


# User Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

def buyer_home(request):  
    return render(request, 'app/buyer.html')

def seller_home(request):
    return render(request, 'app/seller.html')


def  cart_page(request):
    return render (request,  'app/cart.html')

def  checkout_page(request):
    return render (request,  'app/checkout.html')

def product_list(request):
    products = Product.objects.all()  # Fetch all products
    return render(request, 'product_list.html', {'products': products})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new product
            return redirect('product_list')  # Redirect to the product list
    else:
        form = ProductForm()  # Display an empty form

    return render(request, 'add_product.html', {'form': form})

def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)  # Get the product by its ID
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)  # Pre-fill the form with the product's existing data
        if form.is_valid():
            form.save()  # Save the updated product
            return redirect('product_list')  # Redirect to the product list
    else:
        form = ProductForm(instance=product)  # Display the form with existing product data

    return render(request, 'edit_product.html', {'form': form})

def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)  # Get the product by its ID
    if request.method == 'POST':
        product.delete()  # Delete the product
        return redirect('product_list')  # Redirect to the product list
    return render(request, 'delete_product.html', {'product': product})

def role_page(request):
    if request.user.groups.filter(name='Seller').exists():
        return redirect('seller_home')  # Redirect to seller home if the user is a seller
    elif request.user.groups.filter(name='Buyer').exists():
        return redirect('buyer_home')  # Redirect to buyer home if the user is a buyer
    else:
        return render(request, 'app/rolepage.html')  # Show the role selection page

