from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .models import *
from rest_framework import status


# Create your views here.
class MealsAPI(APIView):
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


class OrderedMealsAPI(APIView):
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
            "message": "Successfully retrieved orders!",
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
                    "street": customer.street,
                    "postal_code": customer.postal_code,
                    "city": customer.city,
                },
                "ordered_items": [{"name": item["name"],"amount": item["amount"],} for item in ordered_items],
            },
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
