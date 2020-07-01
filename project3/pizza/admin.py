from django.contrib import admin

from .models import Dish, Order, OrderedDish, Balance
# Register your models here.


class DishAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,  {'fields':['name']}),
        ('Money', {'fields':['price']})
    ]
    list_display = ['name', 'price']
    list_filter = ['price']
    search_fields = ['name']

class OrderedDishesInline(admin.TabularInline):
    model = OrderedDish
    extra = 3

class OrderAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields':['user']}),
        ('Main_Info', {'fields':['cost', 'confirmed']})
    ]
    inlines = [OrderedDishesInline]
    list_display = ('__str__', 'confirmed')
    search_fields = ['user__username']

admin.site.register(Dish, DishAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Balance)
admin.site.register(OrderedDish)
