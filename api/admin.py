from django.contrib import admin
from .models import *
from django.utils.html import format_html
from django.utils.safestring import mark_safe


from django.contrib import admin
from django.utils.html import format_html

from .models import Meals


@admin.register(Meals)
class MealsAdmin(admin.ModelAdmin):
    list_display = ("id","name", "description", "price", "display_image")

    def display_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50px" height="50px" />'.format(obj.image.url)
            )
        return None

    display_image.short_description = "Image"



@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "street", "postal_code", "city"]


@admin.register(OrderedMeals)
class OrderedMealsAdmin(admin.ModelAdmin):
    list_display = ["order_user", "order_date", "order_meals", "amount"]
