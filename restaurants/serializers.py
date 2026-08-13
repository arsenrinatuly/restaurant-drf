from rest_framework import serializers

from .models import Restaurant, Category, MenuItem

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'city']


class CategorySerializer(serializers.ModelSerializer):
    restaurant_name = serializers.CharField(
        source="restaurant.name",
        read_only=True
    )
    class Meta:
        model = Category
        fields = ['id', 'name', 'restaurant', 'restaurant_name']


class MenuItemSerializer(serializers.ModelSerializer):
    def validate_price(self,value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero")
        return value



    category_name = serializers.CharField(
        source="category.name",
        read_only=True
    )
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'price', 'category', 'category_name']