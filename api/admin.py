from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Meals)
class MealsAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "price"]


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["name", "street", "postal_code", "city"]


@admin.register(OrderedMeals)
class OrderedMealsAdmin(admin.ModelAdmin):
    list_display = ["order_user", "order_date", "order_meals", "amount"]
