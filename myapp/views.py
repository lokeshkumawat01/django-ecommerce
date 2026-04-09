from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, F, Count, DecimalField
from django.db.models.functions import TruncMonth
from orders.models import Order, OrderItem
from .models import Product
import json
# Create your views here.


def Index(request):
    products = Product.objects.all()
    return render(request, 'myapp/index.html',{'products':products})


def detail(request, slug):
    product = Product.objects.get(slug=slug)
    return render(request, 'myapp/details.html', {'product':product})

def all_products(request):
    products = Product.objects.all()

    query = request.GET.get('q')
    if query:
        products = products.filter(name__icontains=query)

    category = request.GET.get('category')
    if category:
        products = products.filter(category__iexact=category)

    return render(request, 'myapp/all_products.html', {
        'products': products
    })


def track_order_page(request):
    order = None
    error_message = None
    
    # Jab user form submit karega, tab URL mein ?order_id=ORD-... aayega
    search_query = request.GET.get('order_id')
    
    if search_query:
        # Search query ko clean karna (spaces hatana)
        search_query = search_query.strip()
        try:
            # Database mein check karo ki kya ye ID exist karti hai
            order = Order.objects.get(order_id=search_query)
        except Order.DoesNotExist:
            error_message = "Sorry! No order found with this Tracking ID. Please check again."

    context = {
        'order': order,
        'error': error_message,
        'search_query': search_query # Taaki search box mein ID likhi hui reh jaye
    }
    return render(request, 'myapp/track_order.html', context)


###################################################### Admin Dashboard ################################################################


@staff_member_required
def custom_dashboard(request):
    total_sales_dict = Order.objects.filter(is_paid=True).aggregate(Sum('total_amount'))
    total_sales = total_sales_dict['total_amount__sum'] or 0

    profit_dict = OrderItem.objects.filter(order__is_paid=True).aggregate(
        total_profit=Sum(
            (F('product__price') - F('product__cost_price')) * F('quantity'),
            output_field=DecimalField()
        )
    )
    total_profit = profit_dict['total_profit'] or 0

    total_orders = Order.objects.count()
    returned_orders = Order.objects.filter(status='Cancelled').count() 
    return_rate = round((returned_orders / total_orders * 100), 1) if total_orders > 0 else 0

 
    loss_making_products = Product.objects.filter(cost_price__gt=F('price'))


    top_products = OrderItem.objects.filter(order__is_paid=True)\
        .values('product__name', 'product__price', 'product__cost_price')\
        .annotate(total_sold=Sum('quantity'))\
        .order_by('-total_sold')[:5] # Top 5 products


    monthly_sales = Order.objects.filter(is_paid=True)\
        .annotate(month=TruncMonth('created_at'))\
        .values('month')\
        .annotate(revenue=Sum('total_amount'))\
        .order_by('month')

    months_list = [entry['month'].strftime('%b %Y') for entry in monthly_sales] if monthly_sales else ['No Data']
    revenue_list = [float(entry['revenue']) for entry in monthly_sales] if monthly_sales else [0]

    context = {
        'total_sales': f"₹{total_sales:,.2f}",
        'total_profit': f"₹{total_profit:,.2f}",
        'total_orders': total_orders,
        'return_rate': f"{return_rate}%",
        'loss_products_count': loss_making_products.count(),
        'loss_products': loss_making_products,
        'top_products': top_products,
        
       
        'months_json': json.dumps(months_list),
        'revenue_json': json.dumps(revenue_list),
    }

    return render(request, 'myapp/admin_dashboard.html', context)