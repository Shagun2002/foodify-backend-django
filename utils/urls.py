from django.urls import path
from . import views

urlpatterns = [
    path("contact-us/", views.ContactUsAPI.as_view(), name="contact-us"),
    path("book-table/", views.BookTableAPI.as_view(), name="book-table"),
    
]
