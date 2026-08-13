from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Restaurant, Category, MenuItem
from .serializers import RestaurantSerializer, CategorySerializer, MenuItemSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.views.decorators.csrf import csrf_exempt


import json



@api_view(["GET", "POST"])
def menu_items_list(request):
    if request.method == "GET":
        menu_items = MenuItem.objects.all()
        serializer = MenuItemSerializer(menu_items, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer_post = MenuItemSerializer(data=request.data)
        serializer_post.is_valid(raise_exception=True)
        serializer_post.save()

        return Response(serializer_post.data, status=201)


@api_view(["GET", "PATCH", "DELETE"])
def menu_items_detail(request, menu_item_id):

    menu_item = get_object_or_404(MenuItem, id=menu_item_id)

    if request.method == "GET":
        serializer = MenuItemSerializer(menu_item)
        return Response(serializer.data)

    elif request.method == "DELETE":
        menu_item.delete()
        return Response({"message": "deleted"})

    elif request.method == "PATCH":
        serializer_patch = MenuItemSerializer(instance=menu_item, data=request.data, partial=True)
        serializer_patch.is_valid(raise_exception=True)
        serializer_patch.save()
        return Response(serializer_patch.data, status=200)




@api_view(["GET", "POST"])
def categories_list(request):
    if request.method == "GET":
        categories = Category.objects.all()
        serializer = CategorySerializer(categories,many=True)

        return Response(serializer.data)

    elif request.method == "POST":
        data = request.data
        serializer_post = CategorySerializer(data=data)
        serializer_post.is_valid(raise_exception=True)
        serializer_post.save()

        return Response(serializer_post.data, status=201)


@api_view(["PATCH", "DELETE", "GET"])
def categories_detail(request, category_id):

    category = get_object_or_404(Category, id=category_id)

    if request.method == "GET": 
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    elif request.method == "PATCH":


        serializer_patch = CategorySerializer(instance=category, partial=True, data=request.data)
        serializer_patch.is_valid(raise_exception=True)
        serializer_patch.save()

        return Response(serializer_patch.data)

    elif request.method == "DELETE":
        category.delete()

        return Response({"message": "deleted"}, status=200)

        


# Create your views here.
@api_view(["GET", "POST"])
def restaurants_list(request):
    if request.method == 'GET':
        restaurants = Restaurant.objects.all()
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data
        serializer_post = RestaurantSerializer(data=data)
        serializer_post.is_valid(raise_exception=True)
        serializer_post.save()
        return Response(serializer_post.data, status=201)


@api_view(["GET", "DELETE", "PATCH"])
def restaurants_detail(request , restaurant_id):

    restaurant = get_object_or_404(Restaurant, id=restaurant_id)


    if request.method == "GET":


        serializer = RestaurantSerializer(restaurant)

        return Response(serializer.data)
    
    elif request.method == "DELETE":
        
        restaurant.delete()
        return Response({"message": "Deleted."}, status=200)
    
    elif request.method == "PATCH":
        serializer_patch = RestaurantSerializer(partial=True, instance=restaurant, data=request.data)
        serializer_patch.is_valid(raise_exception=True)
        serializer_patch.save()
        return Response(serializer_patch.data)