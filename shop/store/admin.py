from django.contrib import admin
from .models import *
from .forms import *
# Register your models here.


admin.site.register(Products)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(ShippingAddress)
