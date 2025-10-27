from django.db import models
from django_jalali.db import models as jmodels
from django.core.validators import MinValueValidator

class Customer(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام کامل")
    phone = models.CharField(max_length=15, verbose_name="شماره تماس", blank=True)
    address = models.TextField(verbose_name="آدرس کامل", blank=True)
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    
    class Meta:
        verbose_name = "مشتری"
        verbose_name_plural = "مشتریان"
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام محصول")
    size = models.CharField(max_length=10, verbose_name="سایز")
    color = models.CharField(max_length=20, verbose_name="رنگ")
    price = models.IntegerField(default=0, validators=[MinValueValidator(0)], verbose_name="قیمت (تومان)")
    stock = models.IntegerField(default=0, verbose_name="موجودی")
    
    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"
    
    def __str__(self):
        return f"{self.name} - سایز {self.size}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', '⏳ در انتظار تایید'),
        ('confirmed', '✅ تایید شده'),
        ('production', '🔧 در حال تولید'),
        ('ready', '📦 آماده ارسال'),
        ('delivered', '🚚 ارسال شده'),
        ('cancelled', '❌ لغو شده'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="مشتری")
    order_date = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ سفارش")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="وضعیت سفارش")
    is_invoice = models.BooleanField(default=False, verbose_name="صورت حساب مشتری")
    notes = models.TextField(blank=True, verbose_name="یادداشت")
    
    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارشات"
    
    def total_amount(self):
        return sum(item.item_amount() for item in self.order_items.all())
    
    def total_pairs(self):
        return sum(item.total_pairs() for item in self.order_items.all())
    
    def __str__(self):
        return f"سفارش {self.id} - {self.customer.name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="محصول")
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)], verbose_name="تعداد (جفت)")
    is_carton = models.BooleanField(default=False, verbose_name="سفارش کارتنی")
    carton_count = models.IntegerField(default=0, verbose_name="تعداد کارتن")
    pairs_per_carton = models.IntegerField(default=0, verbose_name="تعداد جفت در هر کارتن")
    
    class Meta:
        verbose_name = "آیتم سفارش"
        verbose_name_plural = "آیتم‌های سفارش"
    
    def total_pairs(self):
        if self.is_carton:
            return self.carton_count * self.pairs_per_carton
        return self.quantity
    
    def item_amount(self):
        return self.product.price * self.total_pairs()
    
    def __str__(self):
        return f"{self.product.name} - {self.total_pairs()} جفت"