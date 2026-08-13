from django.db import models

# Create your models here.

class Restaurant(models.Model):
    name = models.CharField(verbose_name="name of restaurant", max_length=150)
    city = models.CharField(verbose_name="city of restaurant", max_length=100)

    def __str__(self):
        return self.name 
    
class Category(models.Model):
    name = models.CharField(verbose_name="name of category", max_length=100)
    restaurant = models.ForeignKey(to=Restaurant, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    name = models.CharField(verbose_name="name of menuItem", max_length=150)
    price = models.IntegerField(verbose_name="price of menuItem")
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name