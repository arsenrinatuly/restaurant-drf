from .models import Restaurant, Category, MenuItem

from rest_framework.test import APITestCase
from rest_framework import status

class RestaurantListAPITests(APITestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            city="Astana"
        )

    def test_get_restaurants_returns_200(self):
        response = self.client.get("/restaurants/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data[0]["name"],
            self.restaurant.name
        )
        self.assertEqual(len(response.data), 1)


    def test_create_restaurants_return_201(self):
        data = {
            "name": "New Restaurant",
            "city": "Almaty"
        }
        response = self.client.post(
            "/restaurants/",
            data,
            format = "json"

            )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Restaurant.objects.count(), 2 )


    def test_create_restaurants_return_400(self):
        data = {
            "name" : "New Restaurant",
        }
        response = self.client.post(
            "/restaurants/",
            data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Restaurant.objects.count(), 1)


class MenuItemValidationTests(APITestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            city="Astana"
        )
        self.category = Category.objects.create(
            name="Pizza",
            restaurant=self.restaurant
        )

    def test_post_return_400(self):
        data = {
            "name": "Free pizza",
            "price" : 0,
            "category": self.category.id
        }

        response = self.client.post(
            "/menu-items/",
            data,
            format="json"
        )
        self.assertIn("price", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(MenuItem.objects.count() , 0)

# Create your tests here.
