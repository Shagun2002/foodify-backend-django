from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
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

    
class Customer(models.Model):
    name=models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    street=models.CharField(max_length=200,blank=True)
    postal_code=models.CharField(max_length=7)
    city=models.CharField(max_length=50)
    
   
    
    def __str__(self):
        return self.name
    
class OrderedMeals(models.Model):
    order_meals = models.ForeignKey(Meals, default=None, on_delete=models.CASCADE)
    order_user = models.ForeignKey(Customer, on_delete=models.CASCADE, default=None)
    order_date = models.DateTimeField(default=timezone.now)
    amount = models.IntegerField(default=0)

    def __str__(self):
        return f"Order ID: {self.id}"
    


            

    
    