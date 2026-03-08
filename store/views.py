from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


# PRODUCT LIST + SEARCH
def product_list(request):

    query = request.GET.get('q')

    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()

    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())

    return render(request, 'store/product_list.html', {
        'products': products,
        'cart_count': cart_count
    })


# PRODUCT DETAIL
def product_detail(request, id):

    product = get_object_or_404(Product, id=id)

    return render(request, 'store/product_detail.html', {'product': product})


# ADD TO CART
def add_to_cart(request, id):

    cart = request.session.get('cart', {})

    if str(id) in cart:
        cart[str(id)] += 1
    else:
        cart[str(id)] = 1

    request.session['cart'] = cart

    return redirect('cart')


# CART PAGE
def cart(request):

    cart = request.session.get('cart', {})
    products = []
    total = 0

    for id, quantity in cart.items():

        product = get_object_or_404(Product, id=id)

        product.quantity = quantity
        product.total_price = quantity * product.price

        total += product.total_price

        products.append(product)

    return render(request, 'store/cart.html', {
        'products': products,
        'total': total
    })


# INCREASE QUANTITY
def increase_quantity(request, id):

    cart = request.session.get('cart', {})

    if str(id) in cart:
        cart[str(id)] += 1

    request.session['cart'] = cart

    return redirect('cart')


# DECREASE QUANTITY
def decrease_quantity(request, id):

    cart = request.session.get('cart', {})

    if str(id) in cart:

        cart[str(id)] -= 1

        if cart[str(id)] <= 0:
            del cart[str(id)]

    request.session['cart'] = cart

    return redirect('cart')


# REMOVE PRODUCT
def remove_from_cart(request, id):

    cart = request.session.get('cart', {})

    if str(id) in cart:
        del cart[str(id)]

    request.session['cart'] = cart

    return redirect('cart')


# CHECKOUT
def checkout(request):

    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())

    if request.method == "POST":

        name = request.POST.get('name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')

        for product in products:

           Order.objects.create(
    user=request.user,
    product=product,
    quantity=cart[str(product.id)],
    price=product.price,
    name=name,
    address=address,
    city=city,
    pincode=pincode
)
        request.session['cart'] = {}

        return render(request, 'store/order_success.html')

    return render(request, 'store/checkout.html')


# SIGNUP
def signup(request):

    if request.method == "POST":

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.save()

        return redirect('login')

    return render(request, 'store/signup.html')


# LOGIN
def user_login(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('/')

    return render(request, 'store/login.html')


# LOGOUT
def user_logout(request):

    logout(request)

    return redirect('/')


# ORDER HISTORY
from django.contrib.auth.decorators import login_required

@login_required
def order_history(request):

    orders = Order.objects.filter(user=request.user)

    return render(request,'store/orders.html',{'orders':orders})