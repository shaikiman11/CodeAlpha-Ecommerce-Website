from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Product, Order

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'products/product_detail.html', {'product': product})
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)

    cart = request.session.get('cart', {})

    product_id = str(product.id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    request.session['cart'] = cart

    return redirect('cart')
def cart(request):
    cart = request.session.get('cart', {})

    products = []

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)

        products.append({
            'product': product,
            'quantity': quantity,
            'total': product.price * quantity
        })

    total = sum(item['total'] for item in products)

    return render(request, 'products/cart.html', {
        'products': products,
        'total': total
    })
def place_order(request):
    if not request.user.is_authenticated:
        return redirect('login')

    cart = request.session.get('cart', {})

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)

        total_price = product.price * quantity

        Order.objects.create(
            product=product,
            quantity=quantity,
            total_price=total_price
        )

    request.session['cart'] = {}

    return render(request, 'products/order_success.html')
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            return render(request, 'products/register.html', {
                'error': 'Username already exists.'
            })

        user = User.objects.create_user(
            username=username,
            password=password
        )

        login(request, user)

        return redirect('product_list')

    return render(request, 'products/register.html')
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('product_list')

        return render(request, 'products/login.html', {
            'error': 'Invalid username or password.'
        })

    return render(request, 'products/login.html')
def user_logout(request):
    logout(request)
    return redirect('product_list')