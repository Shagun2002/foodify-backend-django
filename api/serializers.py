from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


class MealsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meals
        fields = ["id", "name", "description", "price"]


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["name", "street", "postal_code", "city"]


class OrderedMealsSerializer(serializers.ModelSerializer):
    order_meals = MealsSerializer()

    class Meta:
        model = OrderedMeals
        fields = ['order_meals', 'order_date', 'amount']

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     if 'order_user' in representation:
    #         representation.pop('order_user')
    #     return representation
 