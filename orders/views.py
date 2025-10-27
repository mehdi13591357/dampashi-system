from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Customer, Product, Order, OrderItem

def home_page(request):
    """صفحه اصلی - ریدایرکت به ادمین"""
    return redirect('/admin/')

def new_order(request):
    """صفحه ثبت سفارش جدید"""
    if request.method == 'POST':
        # ثبت سفارش جدید
        customer_name = request.POST.get('customer_name')
        phone = request.POST.get('phone')
        
        # ایجاد یا پیدا کردن مشتری
        customer, created = Customer.objects.get_or_create(
            name=customer_name,
            defaults={'phone': phone}
        )
        
        # ایجاد سفارش
        new_order = Order.objects.create(customer=customer)
        
        return redirect('order_details', order_id=new_order.id)
    
    products = Product.objects.all()
    return render(request, 'orders/new_order.html', {'products': products})

def order_details(request, order_id):
    """صفحه جزئیات سفارش"""
    order = Order.objects.get(id=order_id)
    return render(request, 'orders/order_details.html', {'order': order})

def get_products(request):
    """API برای دریافت لیست محصولات"""
    products = list(Product.objects.values('id', 'name', 'size', 'color', 'price'))
    return JsonResponse(products, safe=False)

def add_order_item(request):
    """API برای اضافه کردن آیتم به سفارش"""
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity', 1)
        
        order = Order.objects.get(id=order_id)
        product = Product.objects.get(id=product_id)
        
        item = OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity
        )
        
        return JsonResponse({'success': True, 'item_id': item.id})
    
    return JsonResponse({'success': False})
