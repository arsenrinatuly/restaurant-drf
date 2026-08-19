from .models import Restaurant, Category, MenuItem

from rest_framework.test import APITestCase
from rest_framework import status

from django.contrib.auth import get_user_model

User = get_user_model()



class AuthenticationPermissionTests(APITestCase):
    def test_anonymous_user_cannot_create_restaurant(self):
        data = {
            "name": "New Restaurant",
            "city": "Almaty"
        }
        restaurants_count_before = Restaurant.objects.count()
        response = self.client.post(
            "/restaurants/",
            data,
            format = "json"

            )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Restaurant.objects.count(), restaurants_count_before)

    def test_user_can_obtain_token(self):
        password="StrongTestPass123!"
        self.user = User.objects.create_user(
            username="testuser",
            password=password,
        )
        data = {
            "username": "testuser",
            "password" : password,
        }
        response = self.client.post("/api/token/", data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_user_with_token_can_create_restaurant(self):
        password="StrongTestPass123!"
        self.user = User.objects.create_user(
            username="testuser",
            password=password,
        )
        data = {
            "username": "testuser",
            "password" : password,
        }

        data_restaurant = {
            "name": "New Restaurant",
            "city": "Almaty"
        }
        restaurants_count_before = Restaurant.objects.count()


        token_response = self.client.post("/api/token/", data=data, format="json")
        self.assertEqual(
            token_response.status_code, status.HTTP_200_OK,
        )
        token = token_response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        response = self.client.post("/restaurants/",data=data_restaurant, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Restaurant.objects.count(), restaurants_count_before+1)


class RestaurantListAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="StrongTestPass123!",
        )
        self.client.force_authenticate(user=self.user)

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
        self.user = User.objects.create_user(
            username="testuser",
            password="StrongTestPass123!",
        )
        self.client.force_authenticate(user=self.user)

        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            city="Astana"
        )
        self.category = Category.objects.create(
            name="Pizza",
            restaurant=self.restaurant
        )

        self.menu_item = MenuItem.objects.create(
            name="Pepperoni",
            price=1000,
            category=self.category
        )

    def test_put_menu_item_updates_all_fields_returns_200(self):
        data = {
            "name": "Free pizza",
            "price" : 1200,
            "category": self.category.id
        }
        response = self.client.put(f"/menu-items/{self.menu_item.id}/",data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.menu_item.refresh_from_db()
        self.assertEqual(self.menu_item.name, data["name"])
        self.assertEqual(self.menu_item.price, data["price"])
        self.assertEqual(self.menu_item.category_id, data["category"])

    def test_filter_menu_items_by_category(self):
        other_category = Category.objects.create(
            name="Drinks",
            restaurant=self.restaurant,
        )

        MenuItem.objects.create(
            name="Free pizza",
            price=1200,
            category=other_category,
        )
        response = self.client.get("/menu-items/", {"category": self.category.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.menu_item.id)

    def test_search_menu_items_by_name(self):
        MenuItem.objects.create(
            name="Cola",
            price=500,
            category=self.category,
        )
        response = self.client.get("/menu-items/", {"search": "pep"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"],self.menu_item.id)

    def test_order_menu_items_by_price(self):
        cheap = MenuItem.objects.create(
            name="cola",
            price=500,
            category=self.category,
        )
        response = self.client.get("/menu-items/", {"ordering": "price"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["id"], cheap.id)
        self.assertEqual(response.data[1]["id"], self.menu_item.id)
    def test_get_menu_item_detail_returns_200(self):
        response = self.client.get(f"/menu-items/{self.menu_item.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["name"],
            self.menu_item.name,
        )

    def test_patch_menu_item_updates_price_returns_200(self):
        data = {
            "price" : 1500,
        }
        response = self.client.patch(f"/menu-items/{self.menu_item.id}/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["price"], data["price"]
        )
        self.menu_item.refresh_from_db()
        self.assertEqual(
            self.menu_item.price,
            data["price"]
        )

    def test_get_missing_menu_item_returns_404(self):
        missing_id = 99999

        response = self.client.get(f"/menu-items/{missing_id}/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_menu_item_returns_204(self):

        response = self.client.delete(f"/menu-items/{self.menu_item.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(MenuItem.objects.filter(id=self.menu_item.id).exists())


    def test_post_return_400(self):
        data = {
            "name": "Free pizza",
            "price" : 0,
            "category": self.category.id
        }

        items_count_before = MenuItem.objects.count()

        response = self.client.post(
            "/menu-items/",
            data,
            format="json"
        )
        self.assertIn("price", response.data)
        self.assertEqual(MenuItem.objects.count(), items_count_before)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)