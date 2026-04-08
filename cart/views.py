from django.shortcuts import render
from django.http import JsonResponse
from .cart import Cart
from myapp.models import Product
from django.shortcuts import get_object_or_404
# Create your views here.

# In views.py

def cart_add(request):
    # 1. Grab the cart session
    cart = Cart(request)
    
    # 2. Check for the POST request from your AJAX/Frontend
    if request.POST.get('action') == 'post' or request.method == 'POST':
        product_id = request.POST.get('product_id')
        product_qty = request.POST.get('product_quantity')
        
        # 3. Get the actual product from the database
        product = get_object_or_404(Product, id=product_id)
        
        # 4. Call the add method from your cart.py file
        cart.add(product=product, product_qty=product_qty)
        
        # 5. Return a response
        cart_quantity = cart.__len__()
        return JsonResponse({'qty': cart_quantity})


def cart_overview(request):
    cart = Cart(request)
    return render(request, 'cart/cart-overview.html', {'cart':cart})

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'POST':
        product_id = request.POST.get('product_id')
        cart.delete(product_id=product_id)
        cart_quantity = cart.__len__()
        cart_total = cart.get_total_price()
        return JsonResponse({'qty': cart_quantity, 'total': cart_total})
    
def cart_update(request):
    cart = Cart(request)
    if request.method=='POST':
        product_id = request.POST.get('product_id')
        product_quantity = request.POST.get('product_quantity')
        cart.update(product=product_id, qty=product_quantity)
        return JsonResponse({'message': 'Cart updated successfully'})
