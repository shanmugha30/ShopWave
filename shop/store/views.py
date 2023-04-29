from django.shortcuts import render,redirect,get_object_or_404
from . forms import *
from django.contrib.auth import authenticate,login,logout
from .models import *
# Create your views here.


def home(request):
    products = Products.objects.filter(featured_product=True)
    return render(request,"home.html",{'products':products})


def signUp(request):
    form=UserCreateForm()
    if request.method == "POST":
        form=UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('log_in')
    context={
        'form':form
    }
    return render(request, 'register.html', context)

def loginuser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pwd = request.POST.get('password')
        user = authenticate(request, username=username,password=pwd)
        if user is not None:
            login(request,user)
            return redirect('home')
    return render(request,'login.html',{})

def logoutuser(request):
    logout(request)
    return redirect('log_in')


def storeProducts(request):
    categories=Category.objects.all()
    products=Products.objects.all()
    form = PriceFilterForm()

    if request.method == "POST":
        form = PriceFilterForm(request.POST)
        if form.is_valid():
            min_price = form.cleaned_data.get('min_price')
            max_price = form.cleaned_data.get('max_price')
            products = Products.objects.filter(price__gte=min_price, price__lte=max_price)
    context={
        'products':products,
        'categories':categories,
        'form':form,
    }
    return render(request,'store.html',context)

def cart(request):
    if request.user.is_authenticated:
        cart_items = Order.objects.filter(user=request.user)

        items_total=0
        cart_total=0
        for item in cart_items:
            if item.status == False:
                items_total=items_total+item.quantity
                cart_total = cart_total + item.get_total

        context={
            'cart_items':cart_items,
            'cart_total':cart_total,
            'items_total':items_total,
        }
        return render(request,'cart.html',context)
    else:
        return redirect('signup')


def add_to_cart(request,product_id):
    if request.user.is_authenticated:
        cart_item,created=Order.objects.get_or_create(user=request.user,products_id=product_id)

        if not created:
            cart_item.quantity+=1
            cart_item.save()
            print(cart_item.quantity)
        elif created:
            cart_item.quantity=1
            cart_item.save()
        return redirect('store_products')
    else:
        return redirect('log_in')


def increase_quantity(request,product_id):
    cart_item = Order.objects.get(products_id=product_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_content')


def decrease_quantity(request, product_id):
    cart_item = Order.objects.get(products_id=product_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart_content')


def get_categories(request,category_id):
    categories = Category.objects.all()
    products=Products.objects.order_by('price').filter(category_id=category_id)
    form = PriceFilterForm()

    if request.method == "POST":
        form = PriceFilterForm(request.POST)
        if form.is_valid():
            min_price = form.cleaned_data.get('min_price')
            max_price = form.cleaned_data.get('max_price')
            products = Products.objects.filter(price__gte=min_price, price__lte=max_price)

    context = {
        'products':products,
        'categories':categories,
        'form':form,
    }
    return render(request, 'store.html', context)


def checkout(request):
    orders = Order.objects.filter(user=request.user)
    items_total = 0
    cart_total = 0
    for item in orders:
        if item.status == False:
            items_total = items_total + item.quantity
            cart_total = cart_total + item.get_total
    context={
        'orders':orders,
        'cart_total':cart_total,
        'item_total':items_total,
    }
    return render(request,'checkout.html', context)



def product_detail(request,slug):
    product = get_object_or_404(Products, slug=slug)
    return render(request, 'product_detail.html', {'product': product})






