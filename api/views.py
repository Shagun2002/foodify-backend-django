from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .models import *
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q


class MealsAPI(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        meals = Meals.objects.all()
        serializer = MealsSerializer(meals, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MealsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": status.HTTP_201_CREATED,
                    "message": "Meals added!",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MealDetailsAPIView(APIView):
    def get(self, request, id):
        try:
            print("id = ", id)
            meal = Meals.objects.get(id=id)
            serializer = MealsSerializer(meal)
            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "message": "Meal details retrieved successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        except Meals.DoesNotExist:
            return Response(
                {
                    "status": status.HTTP_404_NOT_FOUND,
                    "message": "Meal not found",
                },
                status=status.HTTP_404_NOT_FOUND,
            )


class OrderedMealsAPI(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request, name):
        orders = OrderedMeals.objects.filter(order_user__name=name)
        if not orders:
            return Response(
                {
                    "status": status.HTTP_404_NOT_FOUND,
                    "message": "No orders found!",
                    "data": None,
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        order_user = orders.first().order_user
        order_user_serializer = CustomerSerializer(order_user)

        serializer = OrderedMealsSerializer(orders, many=True)

        data = {
            "status": status.HTTP_200_OK,
            "message": "Successfully retrieved Orders!",
            "data": {
                "user_info": order_user_serializer.data,
                "orders": serializer.data,
            },
        }
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        ordered_items = request.data.get("ordered_items", [])
        user_info_data = request.data.get("user_info", {})

        if not ordered_items:
            return Response(
                {"detail": "No Order Items"}, status=status.HTTP_400_BAD_REQUEST
            )

        customer_serializer = CustomerSerializer(data=user_info_data)
        customer_serializer.is_valid(raise_exception=True)
        customer = customer_serializer.save()

        ordered_meals = []
        for item in ordered_items:
            meal = Meals.objects.filter(name=item["name"]).first()
            print("meal = ", meal)
            if not meal:
                return Response(
                    {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "No meals Found!",
                        "data": None,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            ordered_meal = OrderedMeals(
                order_meals=meal, order_user=customer, amount=item["amount"]
            )
            ordered_meals.append(ordered_meal)

        OrderedMeals.objects.bulk_create(ordered_meals)

        response_data = {
            "status": status.HTTP_201_CREATED,
            "message": "Order placed successfully!",
            "data": {
                "user_info": {
                    "name": customer.name,
                    "email": customer.email,
                    "street": customer.street,
                    "postal_code": customer.postal_code,
                    "city": customer.city,
                },
                "ordered_items": [
                    {
                        "name": item["name"],
                        "amount": item["amount"],
                    }
                    for item in ordered_items
                ],
            },
        }
        return Response(response_data, status=status.HTTP_201_CREATED)


class SearchAPIView(APIView):
    def get(self, request, name):
        searched_meal = Meals.objects.all().filter(Q(name__icontains=name))

        if searched_meal.exists():
            serializer = MealsSerializer(searched_meal, many=True)
            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "message": "Meals FOUND successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "status": status.HTTP_404_NOT_FOUND,
                    "message": "No similar meal found!",
                },
                status=status.HTTP_404_NOT_FOUND,
            )


class ReviewRatingAPI(APIView):
    def get(self, request):
        review = ReviewRating.objects.all()
        serializer = ReviewRatingSerializer(review, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReviewRatingSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                {
                    "status": status.HTTP_201_CREATED,
                    "message": "Review ratings added!",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {
                "status": status.HTTP_404_NOT_FOUND,
                "message": "ERROR while posting review Ratings!",
            },
            status=status.HTTP_404_NOT_FOUND,
        )


def admin_only(func):
    def wrapper(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == "Admin":
            return func(self, request, *args, **kwargs)
        return Response(
            {"message": "Unauthorized user"}, status=status.HTTP_401_UNAUTHORIZED
        )

    return wrapper


class TestimonialsAPI(APIView):
    def get(self, request):
        testimonials = Testimonials.objects.all()
        serializer = TestimonialsSerializer(testimonials, many=True)
        if len(serializer.data) != 0:
            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "message": "Got all the testimonials",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "status": status.HTTP_404_NOT_FOUND,
                    "message": "ERROR in getting the Testimonials",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

    @admin_only
    def post(self, request):
        serializer = TestimonialsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": status.HTTP_201_CREATED,
                    "message": "Testimonial added successfully!",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @admin_only
    def put(self, request, id):
        try:
            testimonial = Testimonials.objects.get(id=id)
        except Testimonials.DoesNotExist:
            return Response(
                {"message": "Testimonial not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = TestimonialsSerializer(testimonial, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "message": "Testimonial updated successfully!",
                    "data": serializer.data,
                }
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @admin_only
    def delete(self, request, id):
        try:
            testimonial = Testimonials.objects.get(id=id)
        except Testimonials.DoesNotExist:
            return Response(
                {"message": "Testimonial not found"}, status=status.HTTP_404_NOT_FOUND
            )

        testimonial.delete()
        return Response(
            {"message": f"Testimonial{id} deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
