from django.urls import path, include
from . import views

urlpatterns = [
    path("meals/", views.MealsAPI.as_view(), name="meals"),
    path("orders/", views.OrderedMealsAPI.as_view(), name="orders"),
    path("orders/<str:name>", views.OrderedMealsAPI.as_view(), name="orders-get"),
]
