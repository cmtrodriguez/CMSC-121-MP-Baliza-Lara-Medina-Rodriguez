from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Renders buyer homepage
@login_required
def buyer_home(request):  
    return render(request, 'app/buyer.html')

# Renders seller homepage
@login_required
def seller_home(request):
    return render(request, 'app/seller.html')

# Renders role selection page
@login_required
def role_page(request):
    user = request.user
    return render(request, 'app/rolepage.html', {'user': user})

# Renders cart page
@login_required
def cart_page(request):
    return render(request, 'app/cart.html')

# Renders checkout page
@login_required
def checkout_page(request):
    return render(request, 'app/checkout.html')

from django.contrib.auth.models import User

def signup(request):
    if request.method == "POST":
        full_name = request.POST.get('name')  # your form sends 'name'
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Simple splitting of full name (adjust as needed)
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

        # username is required, use email or something unique
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





from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Django's default User model uses username to authenticate,
        # so you need to find username by email first
        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            return redirect('role_page')  # or wherever you want
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('login')

    return render(request, 'app/login.html')


from django.contrib.auth import logout

def logout_view(request):
    logout(request)  # logs out user properly
    return redirect('login')
