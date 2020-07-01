from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Balance, Dish, Order
from urllib.parse import unquote
# Create your views here.

def user_cabinet(request):
    if request.user.is_authenticated:
        user_info = {
        'username':request.user.username,
        'balance':Balance.objects.filter(user=request.user).first().money_amount,
        'date_joined': request.user.date_joined
        }
    else:
        return HttpResponseRedirect(reverse('pizza:log_in'))

    context = {
        'page_name': 'Personal Cabinet',
        'user_info': user_info,
    }
    return render(request, 'pizza/user_cabinet.html', context)

def index(request):
    if request.user.is_authenticated:

        user_info = {
        'username':request.user.username,
        'balance':Balance.objects.filter(user=request.user).first().money_amount
        }

    else:
        user_info = None

    context = {
        'page_name': 'HOME',
        'user_info': user_info
    }
    print(request.user.username)
    return render(request, 'pizza/index.html', context)

def menu(request):
    if request.user.is_authenticated:
        user_info = {
        'username':request.user.username,
        'balance':Balance.objects.filter(user=request.user).first().money_amount
        }
    else:
        user_info = None

    dishes = Dish.objects.all()

    context = {
        'page_name': 'MENU',
        'dishes':dishes,
        'dishes_names':[dish.name for dish in dishes],
        'user_info': user_info
    }
    return render(request, 'pizza/menu.html', context)

def location(request):
    if request.user.is_authenticated:
        user_info = {
        'username':request.user.username,
        'balance':Balance.objects.filter(user=request.user).first().money_amount
        }
    else:
        user_info = None

    context = {
        'page_name': 'LOCATION',
        'user_info': user_info
    }
    return render(request, 'pizza/location.html', context)

def work_time(request):
    if request.user.is_authenticated:
        user_info = {
        'username':request.user.username,
        'balance':Balance.objects.filter(user=request.user).first().money_amount
        }
    else:
        user_info = None

    context = {
        'page_name': 'WORK TIME',
        'user_info': user_info
    }
    return render(request, 'pizza/work_time.html', context)

def dish(request, dish_name):
    if request.user.is_authenticated:
        user_info = {
        'username':request.user.username,
        'balance':Balance.objects.filter(user=request.user).first().money_amount
        }
    else:
        user_info = None

    context = {
        'page_name': 'WORK TIME',
        'user_info': user_info,
        'dish':Dish.objects.filter(name=dish_name).first()
    }
    return render(request, 'pizza/dish.html', context)

# bay system
def basket(request):
    if request.user.is_authenticated:
        user_info = {
        'username':request.user.username,
        'balance':Balance.objects.filter(user=request.user).first().money_amount
        }
        context = {
            'page_name': 'LOCATION',
            'user_info': user_info,
            'ordered_dishes':request.user.orders.filter(confirmed=False).first().ordered_dishes.all(),
            'order_cost':request.user.orders.filter(confirmed=False).first().cost
        }
        return render(request, 'pizza/basket.html', context)
    else:
        return HttpResponseRedirect(reverse('pizza:index'))


def add_to_order(request, dish_name):
    if request.method == 'POST' and request.user.is_authenticated:
        user= request.user
        order = user.orders.filter(confirmed=False).first()
        order.add_dish(Dish.objects.filter(name=dish_name).first())
        order.save()
        return HttpResponseRedirect(reverse('pizza:basket'))
    elif not request.user.is_authenticated:
        return HttpResponse('log in before ordering')
    else:
        return HttpResponse('Unexpected request')

def delete_from_basket(request, dish_name):
    if request.method == 'POST' and request.user.is_authenticated:
        user = request.user
        dish = Dish.objects.filter(name=dish_name)
        order = user.orders.filter(confirmed=False).first()
        ordered_dish = order.ordered_dishes.filter(dish=Dish.objects.filter(name=dish_name).first()).first()
        order.cost -= ordered_dish.dish.price * ordered_dish.amount
        order.save()
        ordered_dish.delete()
        return HttpResponseRedirect(reverse('pizza:basket'))
    else:
        return HttpResponse('Unexpected request')

def confirm_order(request):
    if request.method == 'POST' and request.user.is_authenticated:
        user = request.user
        order = user.orders.filter(confirmed=False).first()
        balance = user.balance.first()
        if balance.money_amount < order.cost:
            return HttpResponse('not enough money')
        order.confirmed=True
        order.save()
        Order.objects.create(user=user)
        balance.money_amount -= order.cost
        balance.save()
        return HttpResponseRedirect(reverse('pizza:basket'))
    else:
        return HttpResponse('Unexpected request')

def update_balance(request):
    if request.user.is_authenticated:
        user_info = {
        'username':request.user.username,
        'balance':Balance.objects.filter(user=request.user).first().money_amount
        }
        context = {
            'page_name': 'WORK TIME',
            'user_info': user_info,
        }
        return render(request, 'pizza/update_balance.html', context)
    else:
        return HttpResponseRedirect(reverse('pizza:log_in'))

def update_user_balance(request):
    if request.user.is_authenticated and request.method == 'POST':
        money_amount = int(request.POST['money_amount'])
        balance = Balance.objects.filter(user=request.user).first()
        balance.money_amount += money_amount
        balance.save()

        return HttpResponseRedirect(reverse('pizza:user_cabinet'))
    else:
        return HttpResponseRedirect(reverse('pizza:index'))
# authenticate system
def sign_up(request):
    if not request.user.is_authenticated:
        return render(request, 'pizza/register_or_login.html', {'page_type':'sign_up'})
    else:
        return HttpResponseRedirect(reverse('pizza:user_cabinet'))

def log_in(request):
    if not request.user.is_authenticated:
        return render(request, 'pizza/register_or_login.html', {'page_type':'sign_in'})
    else:
        return HttpResponseRedirect(reverse('pizza:index'))

def sign_up_user(request):
    if request.method == 'POST' and not request.user.is_authenticated:
        username = request.POST['username']
        password = request.POST['password']
        print(password)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if user is not None:
            return HttpResponse('username is alreadt taken')
        elif password == request.POST['password_confirm'] and password != '':
            new_user = User.objects.create_user(username=username, password=password)
            Balance.objects.create(user=new_user)
            Order.objects.create(user=new_user)
            return HttpResponse(f'you\'ve just creater an user')
        else:
            return HttpResponse('passwords don\'t match or there was no password')
    elif request.user.is_authenticated:
        return HttpResponseRedirect(reverse('pizza:personal_cabinet'))
    else:
        return HttpResponse('Unexpected request')


def log_in_user(request):
    if request.method == 'POST' and not request.user.is_authenticated:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is None:
            return HttpResponseRedirect(reverse('pizza:log_in'))
        else:
            login(request, user, backend=None)
            return HttpResponseRedirect(reverse('pizza:index'))
    else:
        return HttpResponseRedirect(reverse('pizza:log_in'))

def log_out(request):
    if request.user.is_authenticated:
        logout(request)
    return HttpResponseRedirect(reverse('pizza:index'))
