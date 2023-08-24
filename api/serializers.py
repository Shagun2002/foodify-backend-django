from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


class MealsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meals
        fields = ["id", "name", "description", "price", "image"]


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["name", 'email', "street", "postal_code", "city"]


class OrderedMealsSerializer(serializers.ModelSerializer):
    order_meals = MealsSerializer()

    class Meta:
        model = OrderedMeals
        fields = ['order_meals', 'order_date', 'amount']
    
class ReviewRatingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')
    
    class Meta:
        model=ReviewRating
        fields=['user','meals','comment','rate','created_at']
        
    def create(self, validated_data):
        user = self.context["request"].user
        user_info = CustomUser.objects.get(email=user)
        validated_data["user"] = user_info  #user field of model
        return super().create(validated_data)
    
    

class TestimonialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonials
        fields = [ "id", "image","description", "name"]
    
    
    