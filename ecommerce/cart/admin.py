from django.contrib import admin
from cart.models import Cart,Account,Order
from django.http import HttpResponse
# Register your models here.



admin.site.register(Cart)
admin.site.register(Account)
admin.site.register(Order)