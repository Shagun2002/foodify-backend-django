from rest_framework import serializers
from .models import *


class ContactSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source="user.email", read_only=True)
    class Meta:
        model = ContactUs
        fields = ["user_email", "name", "message", "ratings"]
    

class BookTableSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source="user.email", read_only=True)
    class Meta:
        model = BookTable
        fields = ["user_email", "name", "number_of_persons", "date", "time"]
