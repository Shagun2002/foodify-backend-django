from django.urls import path
from . import views

urlpatterns = [
    path("api/meals/", views.MealsAPI.as_view(), name="meals"),
    path("api/meals/<int:id>/", views.MealDetailsAPIView.as_view(), name="meals-id"),
    path("api/orders/", views.OrderedMealsAPI.as_view(), name="orders"),
    path("api/orders/<str:name>", views.OrderedMealsAPI.as_view(), name="orders-get"),
    
    path("api/meals/<str:name>/", views.SearchAPIView.as_view(), name="meals-name"),
    path("api/ratings/", views.ReviewRatingAPI.as_view(), name="review-rating"),
    path("api/testimonials/", views.TestimonialsAPI.as_view(), name="testimonials"),
    path("api/testimonials/<int:id>", views.TestimonialsAPI.as_view(), name="testimonials"),
]
