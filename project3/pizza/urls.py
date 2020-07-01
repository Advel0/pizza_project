from django.urls import path

from . import views

app_name = 'pizza'
urlpatterns =[
    path('', views.index, name='index'),
    path('personal_cabinet', views.user_cabinet, name='user_cabinet'),
    path('menu', views.menu, name='menu'),
    path('location', views.location, name='location'),
    path('work_time', views.work_time, name='work_time'),
    path('dish/<str:dish_name>', views.dish, name='dish'),
    path('basket', views.basket, name='basket'),

    path('sign_up', views.sign_up, name='sign_up'),
    path('log_in', views.log_in, name='log_in'),
    path('log_out', views.log_out, name='log_out'),
    path('sign_up_user', views.sign_up_user, name='sign_up_user'),
    path('log_in_user', views.log_in_user, name='log_in_user'),

    path('add_to_order/<str:dish_name>', views.add_to_order, name='add_to_order'),
    path('delete_from_basket/<str:dish_name>', views.delete_from_basket, name='delete_from_basket'),
    path('confirm_order', views.confirm_order, name='confirm_order'),
    path('update_balance', views.update_balance, name='update_balance'),
    path('update_user_balance', views.update_user_balance, name='update_user_balance')
]
