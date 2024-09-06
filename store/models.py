from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.contrib.auth.models  import User 

# Create your models here.
class Product(models.Model) : 
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=100, null= False, blank=False, validators=[MinLengthValidator(3)])
    image = models.ImageField(null=True, blank=True, default="/placeholder.png", upload_to="productImages/")
    brand = models.CharField(max_length=100, null=True, blank=True, validators=[MinLengthValidator(3)])
    category = models.CharField(max_length=100, null=True, blank=True, validators=[MinLengthValidator(3)])
    description = models.TextField(null= True, blank=True)
    rating = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    num_reviews = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    price = models.FloatField(default=0, validators=[MinValueValidator(0)])
    count_in_stock = models.IntegerField(null= False, default=0, validators=[MinValueValidator(0)])    
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) : 
        return self.name 
    
    class Meta : 
        db_table = "Product" 
        constraints = [
            models.UniqueConstraint(fields=["name"], name="unique_product_name"), 
            models.CheckConstraint(check=models.Q(rating__gte=0) & models.Q(rating__lte=5), name='valid_rating_range'),
            models.CheckConstraint(check=models.Q(price__gte=0), name='non_negative_price'),
            models.CheckConstraint(check=models.Q(num_reviews__gte=0), name='non_negative_num_reviews'),
            models.CheckConstraint(check=models.Q(count_in_stock__gte=0), name='non_negative_count_in_stock'),
        ]

class Review(models.Model) :
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    text = models.CharField(max_length=200, null=True, blank=True)
    rating = models.FloatField( default=5, validators=[MinValueValidator(0), MaxValueValidator(5)])
    created_at = models.DateTimeField(default=timezone.now)
    
class Order(models.Model) : 
    payment_methods_choices = [
        (1, "visa"),
        (2, "cache"), 
        (3, "fawry")
    ]
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    payment_method = models.IntegerField(default="visa", choices=payment_methods_choices)
    tax_price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True)
    delivered_at = models.DateTimeField(null=True)
    shipping_price = models.FloatField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    total_price = models.FloatField(default=0)
    
class OrderItems(models.Model) : 
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete= models.CASCADE, related_name="order_items")
    quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    price = models.FloatField(default=0)

class ShippingAddress(models.Model) :
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="shipping_address") 
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100) 
    postal_code = models.IntegerField()