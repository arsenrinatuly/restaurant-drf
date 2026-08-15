from django.urls import path
from .views import (
    RestaurantListCreateAPIView,
    RestaurantRetrieveUpdateDestroyAPIView,
    CategoryListCreateAPIView,
    CategoryRetrieveUpdateDestroyAPIView,
    MenuItemListCreateAPIView,
    MenuItemRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path("restaurants/", RestaurantListCreateAPIView.as_view()),
    path("restaurants/<int:restaurant_id>/", RestaurantRetrieveUpdateDestroyAPIView.as_view()),
    path("categories/", CategoryListCreateAPIView.as_view()),
    path("categories/<int:category_id>/", CategoryRetrieveUpdateDestroyAPIView.as_view()),
    path("menu-items/", MenuItemListCreateAPIView.as_view()),
    path("menu-items/<int:menu_item_id>/", MenuItemRetrieveUpdateDestroyAPIView.as_view())
]