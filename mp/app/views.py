from django.shortcuts import render

# Create your views here.

def login_view(request):
    return render(request, 'app/login.html')  

def signup(request):
    return render(request, 'app/signup.html')

def buyer_home(request):  
    return render(request, 'app/buyer.html')

def seller_home(request):
    return render(request, 'app/seller.html')

def role_page(request):
    return render(request, 'app/rolepage.html')

def  cart_page(request):
    return render (request,  'app/cart.html')

def  checkout_page(request):
    return render (request,  'app/checkout.html')

