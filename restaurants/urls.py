from django.urls import path
from .views import restaurants_list, restaurants_detail, categories_list, categories_detail, menu_items_list, menu_items_detail

urlpatterns = [
    path("restaurants/", restaurants_list),
    path("restaurants/<int:restaurant_id>/", restaurants_detail),
    path("categories/", categories_list),
    path("categories/<int:category_id>/", categories_detail),
    path("menu-items/", menu_items_list),
    path("menu-items/<int:menu_item_id>/", menu_items_detail)
]