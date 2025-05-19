from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Product
from django.core.files.storage import default_storage
from django.views.decorators.http import require_POST
from django.db.models import Q
import json

# Renders buyer homepage
@login_required
def buyer_home(request):  
    products = Product.objects.all()
    return render(request, 'app/buyer.html', {'products': products})

# Renders seller homepage
@login_required
def seller_home(request):
    products = Product.objects.filter(seller=request.user)
    return render(request, 'app/seller.html', {'products': products})

# Renders role selection page
@login_required
def role_page(request):
    user = request.user
    return render(request, 'app/rolepage.html', {'user': user})

# Renders cart page
@login_required
def cart_view(request):
    print(f"Viewing cart. Session: {request.session.items()}")
    
    if 'cart' not in request.session:
        request.session['cart'] = {}
        print("Initialized empty cart in cart view")
    
    cart_items = request.session['cart']
    print(f"Cart items: {cart_items}")
    
    items = []
    total = 0
    
    for product_id, quantity in cart_items.items():
        try:
            product = Product.objects.get(id=product_id)
            items.append({
                'product': product,
                'quantity': quantity
            })
            total += product.price * quantity
            print(f"Added product {product.name} to display list")
        except Product.DoesNotExist:
            print(f"Product {product_id} not found, removing from cart")
            del cart_items[product_id]
            request.session['cart'] = cart_items
            request.session.modified = True
    
    return render(request, 'app/cart.html', {
        'cart_items': items,
        'total': total
    })

# Renders checkout page
@login_required
def checkout_page(request):
    cart_items = request.session.get('cart', {})
    items = []
    total = 0
    
    for product_id, quantity in cart_items.items():
        product = get_object_or_404(Product, id=product_id)
        items.append({
            'product': product,
            'quantity': quantity
        })
        total += product.price * quantity
    
    return render(request, 'app/checkout.html', {
        'cart_items': items,
        'total': total
    })

def signup(request):
    if request.method == "POST":
        full_name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if full_name:
            parts = full_name.strip().split(' ', 1)
            first_name = parts[0]
            last_name = parts[1] if len(parts) > 1 else ''
        else:
            first_name = ''
            last_name = ''

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('signup')

        username = email

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.save()

        messages.success(request, "Account created! You can now log in.")
        return redirect('login')

    return render(request, 'app/signup.html')

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            return redirect('role_page')
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('login')

    return render(request, 'app/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

# Product management views
@login_required
def add_product(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            price = request.POST.get('price')
            category = request.POST.get('category')
            image = request.FILES.get('image')

            product = Product.objects.create(
                name=name,
                price=price,
                category=category,
                seller=request.user
            )

            if image:
                product.image = image
                product.save()

            return JsonResponse({
                'status': 'success',
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': str(product.price),
                    'category': product.category,
                    'image_url': product.image.url if product.image else None
                }
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user)
    
    if request.method == 'POST':
        try:
            product.name = request.POST.get('name')
            product.price = request.POST.get('price')
            product.category = request.POST.get('category')
            
            if 'image' in request.FILES:
                # Delete old image if it exists
                if product.image:
                    default_storage.delete(product.image.path)
                product.image = request.FILES['image']
            
            product.save()
            
            return JsonResponse({
                'status': 'success',
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': str(product.price),
                    'category': product.category,
                    'image_url': product.image.url if product.image else None
                }
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user)
    
    if request.method == 'POST':
        try:
            # Delete the image file if it exists
            if product.image:
                default_storage.delete(product.image.path)
            product.delete()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@login_required
@require_POST
def add_to_cart(request, product_id):
    print(f"Adding product {product_id} to cart")
    print(f"Current session: {request.session.items()}")
    
    if 'cart' not in request.session:
        request.session['cart'] = {}
        print("Initialized empty cart")
    
    cart = request.session['cart']
    try:
        product = Product.objects.get(id=product_id)
        print(f"Found product: {product.name}")
        
        if str(product_id) in cart:
            cart[str(product_id)] += 1
            print(f"Increased quantity to {cart[str(product_id)]}")
        else:
            cart[str(product_id)] = 1
            print(f"Added new item with quantity 1")
        
        request.session['cart'] = cart
        request.session.modified = True
        print(f"Updated session cart: {request.session['cart']}")
        
        return JsonResponse({'status': 'success'})
    except Product.DoesNotExist:
        print(f"Product {product_id} not found")
        return JsonResponse({'status': 'error', 'message': 'Product not found'})
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required
@require_POST
def update_cart(request, product_id):
    cart = request.session.get('cart', {})
    quantity = int(request.POST.get('quantity', 1))
    
    if str(product_id) in cart:
        cart[str(product_id)] = quantity
        request.session['cart'] = cart
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error', 'message': 'Product not found in cart'})

@login_required
@require_POST
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error', 'message': 'Product not found in cart'})
