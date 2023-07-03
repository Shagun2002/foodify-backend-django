from django.db import models
from accounts.models import CustomUser
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your models here.
from django.contrib.auth import get_user_model
CustomUser = get_user_model()


class ContactUs(models.Model):
    RATINGS_CHOICES = (
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="contact_us")
    name = models.CharField(max_length=100)
    message = models.TextField(max_length=100)
    ratings = models.CharField(max_length=2, choices=RATINGS_CHOICES)

class BookTable(models.Model):
    PERSON_CHOICES = (
        ("1", "1 person"),
        ("2", "2 persons"),
        ("3", "3 persons"),
        ("4", "4 persons"),
        ("5", "5 persons"),
        ("6", "6 persons"),
        ("7", "7 persons"),
        ("8", "8 persons"),
    )

    TIME_CHOICES = (
        ("06:00 pm", "06:00 pm"),
        ("07:00 pm", "07:00 pm"),
        ("08:00 pm", "08:00 pm"),
        ("09:00 pm", "09:00 pm"),
        ("10:00 pm", "10:00 pm"),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name="book_table")
    name = models.CharField(max_length=10)
    number_of_persons = models.CharField(max_length=2, choices=PERSON_CHOICES)
    
    def validate_date(value):
        if value < timezone.now().date():
            raise ValidationError("Date must be today or later.")

    date = models.DateField(validators=[validate_date])    
    time = models.CharField(max_length=10, choices=TIME_CHOICES)

    def __str__(self):
        return f"{self.number_of_persons} - {self.date} - {self.time}"
