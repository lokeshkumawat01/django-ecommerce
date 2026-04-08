from django.shortcuts import render
from .models import Product
# Create your views here.


def Index(request):
    products = Product.objects.all()
    return render(request, 'myapp/index.html',{'products':products})


def detail(request, slug):
    product = Product.objects.get(slug=slug)
    return render(request, 'myapp/details.html', {'product':product})

def all_products(request):
    products = Product.objects.all() 
    return render(request, 'myapp/all_products.html', {'products': products})