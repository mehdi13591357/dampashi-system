from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('new-order/', views.new_order, name='new_order'),
    path('order/<int:order_id>/', views.order_details, name='order_details'),
    path('api/products/', views.get_products, name='get_products'),
    path('api/add-item/', views.add_order_item, name='add_item'),
]