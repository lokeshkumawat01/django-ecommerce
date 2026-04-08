from django.shortcuts import render, redirect
from myapp.models import Product
from .form import AddressForm
from .models import Address, Order, OrderItem
from cart.cart import Cart
from django.http import JsonResponse
# Create your views here.

def add_address(request):
    # 1. Purana address dhoondo. Agar nahi hai toh 'address' None hoga.
    address = Address.objects.filter(user=request.user).last()

    if request.method == 'POST':
        # 2. Agar address None hai, toh Django naya record banayega.
        # Agar address exist karta hai, toh usi ko update karega.
        form = AddressForm(request.POST, instance=address)
        
        if form.is_valid():
            address_obj = form.save(commit=False)
            address_obj.user = request.user
            address_obj.save()
            
            # Save ke baad seedha checkout page
            return redirect('checkout') 
        else:
            print(form.errors)
    else:
        # 3. Naye user ke liye khali form, purane user ke liye bhara hua form
        form = AddressForm(instance=address)

    return render(request, 'orders/add_address.html', {'form': form})


def checkout(request):
    cart = Cart(request)

    context = {
        'cart': cart,
        'total': cart.get_total_price()
    }

    if request.user.is_authenticated:
        try:
            address = Address.objects.filter(user=request.user).last()
            context['address'] = address
        except Address.DoesNotExist:
            context['address'] = None
            context['error'] = "Please add an address before checkout."
    else:
        context['address'] = None

    return render(request, 'orders/checkout.html', context)
    

def place_order(request):
    if request.method == "POST":
        cart = Cart(request)
        total_amount = cart.get_total_price()

        if not cart:
            return JsonResponse({'success': False})

        # create order
        if request.user.is_authenticated:
            order = Order.objects.create(
                user=request.user,
                total_amount=total_amount
            )
        else:
            order = Order.objects.create(
                total_amount=total_amount
            )

        # create order items
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['qty']
            )

        # 🔥 IMPORTANT: clear cart
        request.session['cart'] = {}

        return JsonResponse({
            'success': True,
            'redirect_url': 'ordersz/order_success/'
        })


def order_success(request):
    return render(request, 'orders/order_success.html')


def order_failed(request):
    return render(request, 'orders/order_failed.html')

def buy_now(request, id):
    product = Product.objects.get(id=id)

    cart = {}

    cart[str(id)] = {
        'price': str(product.price),
        'qty': 1
    }

    request.session['cart'] = cart

    return redirect('checkout')