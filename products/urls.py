from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.index, name="index"),
    path('sell/', views.sell, name="sell"),
    path('sell/product/', views.sell_product, name="sell_product"),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'), 
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('about/', views.about, name='about'),
]

