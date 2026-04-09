from django.urls import path
from . import views


urlpatterns = [
    path('add-address/', views.add_address, name='add_address'),
    path('checkout/', views.checkout, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
    path('order-success/', views.order_success, name='order_success'),
    path('order-failed/', views.order_failed, name='order_failed'),
    path('buy/<int:id>/', views.buy_now, name='buy_now'),
    path('order-history/', views.order_history, name='order_history'),
    path('track-order/', views.track_order_page, name='track_order'),

]
