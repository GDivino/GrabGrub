from django.contrib import admin
from .models import Order, Food, Customer, Account

# Register your models here.
admin.site.register(Account)
admin.site.register(Order)
admin.site.register(Food)
admin.site.register(Customer)