from django.urls import path
from .import views
urlpatterns = [
    path('', views.Index, name='index'),
    path('<slug:slug>', views.detail, name='detail'),
    path('products/', views.all_products, name='all_products'),
    # urls.py mein
    
    path('royal-admin/', views.custom_dashboard, name='custom_dashboard'),
]
