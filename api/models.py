from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from accounts.models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

from django.contrib.auth import get_user_model
CustomUser = get_user_model()


class Meals(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, blank=True)
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to='meals/')

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Meals"

    
class Customer(models.Model):
    name=models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    street=models.CharField(max_length=200,blank=True)
    postal_code=models.CharField(max_length=7)
    city=models.CharField(max_length=50)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Customer"
    
class OrderedMeals(models.Model):
    order_meals = models.ForeignKey(Meals, default=None, on_delete=models.CASCADE)
    order_user = models.ForeignKey(Customer, on_delete=models.CASCADE, default=None)
    order_date = models.DateTimeField(default=timezone.now)
    amount = models.IntegerField(default=0)

    def __str__(self):
        return f"Order ID: {self.id}"
    class Meta:
        verbose_name = "Ordered Meals"
    
class ReviewRating(models.Model):   
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE, default=None)
    meals=models.ForeignKey(Meals, on_delete=models.CASCADE, default=None)
    comment=models.TextField()
    rate=models.FloatField(default=0, validators=[MinValueValidator(0.5), MaxValueValidator(5.0)])
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.comment
    class Meta:
        verbose_name = "Review Ratings"
    
class Testimonials(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='testimonials/')
    description = models.TextField()

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Testimonials"
    


            

    
    