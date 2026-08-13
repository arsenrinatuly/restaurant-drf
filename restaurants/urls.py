from django.urls import path
from .views import categories_list, categories_detail, menu_items_list, menu_items_detail, RestaurantListAPIView, RestaurantDetailAPIView

urlpatterns = [
    path("restaurants/", RestaurantListAPIView.as_view()),
    path("restaurants/<int:restaurant_id>/", RestaurantDetailAPIView.as_view()),
    path("categories/", categories_list),
    path("categories/<int:category_id>/", categories_detail),
    path("menu-items/", menu_items_list),
    path("menu-items/<int:menu_item_id>/", menu_items_detail)
]