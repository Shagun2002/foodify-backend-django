from django.urls import path
from . import views

urlpatterns = [
    path("api/meals/", views.MealsAPI.as_view(), name="meals"),
    path("api/meals/<str:id>/", views.MealDetailsAPIView.as_view(), name="meals-id"),
    path("api/orders/", views.OrderedMealsAPI.as_view(), name="orders"),
    path("api/orders/<str:name>", views.OrderedMealsAPI.as_view(), name="orders-get"),
]
