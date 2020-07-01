from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class Balance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='balance')
    money_amount = models.IntegerField(default=0)

    def __str__(self):
        return f'User: {self.user.username}. Balance:{self.money_amount}'

    def increase(self, amount):
        self.money_amount+=amount


class Dish(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()

    def __str__(self):
        return f' Dish: {self.name}, {self.price}$'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    cost = models.IntegerField(default=0)
    confirmed = models.BooleanField(default=False)

    def add_dish(self, dish):
        if OrderedDish.objects.filter(dish=dish, order=self):
            ordered_dish = OrderedDish.objects.filter(dish=dish, order=self).first()
            ordered_dish.amount += 1
            ordered_dish.save()
        else:
            ordered_dish = OrderedDish(dish=dish, order=self)
            ordered_dish.save()

        self.cost += dish.price
        self.save()

    def delete_dish(self, dish):
        pass

    def confirm_order(self):
        self.confirmed = True

    def __str__(self):
        return f'Order #{self.id}. Dishes: % to do % , Costs: {self.cost}'

class OrderedDish(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)
    order = models.ForeignKey(Order, related_name='ordered_dishes', on_delete=models.CASCADE)

    def __str__(self):
        return f'Ordered dish: {self.dish}, amount:{self.amount}'
# from pizza.models import Dish, OrderedDish, Order, Balance
