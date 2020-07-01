from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import login
from .models import Balance, Dish, Order, OrderedDish
from django.contrib.auth.models import User

class BalanceModelTest(TestCase):
    def test_balance_increase(self):
        user = User('advel', 'dawdaw21e2s')
        balance = Balance(user)
        balance.increase(100)
        self.assertIs(balance.money_amount, 100)

class OrderModelTest(TestCase):
    def test_add_dish(self):
        dish = Dish.objects.create(name='pizza',price= 25)
        user = User.objects.create_user('advel', 'dawdaw21e2s')
        order = Order.objects.create(user=user)
        order.add_dish(dish)
        self.assertIs(len(order.ordered_dishes.all()), 1)

class IntexViewModelTests(TestCase):

    def test_user(self):
        user = User.objects.create_user('advel', 'dawdaw21e2s')
        Balance.objects.create(user=user)
        self.client.force_login(user=user)
        response = self.client.get(reverse('pizza:index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user_info']['username'], 'advel')
