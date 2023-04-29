from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import datetime
import random
# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.name

class Products(models.Model):
    product_name=models.CharField(max_length=100,null=True,blank=True)
    price=models.FloatField()
    slug=models.SlugField(max_length=100,unique=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name="categories")
    product_image=models.ImageField(upload_to='',null=True,blank=True)
    featured_product=models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Products, self).save(*args, **kwargs)


    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Products.objects.filter(category=category_id)
        else:
            return Products.get_all_products()

    def __str__(self):
        return str(self.id)


class Order(models.Model):
    products=models.ForeignKey(Products,on_delete=models.CASCADE,related_name="order_products")
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="users_order")
    quantity=models.IntegerField(null=True,blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    @property
    def get_total(self):
        total=round(self.products.price*self.quantity,2)
        return total

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-date')

    def placeOrder(self):
        self.save()



class ShippingAddress(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_address")
    address=models.CharField(max_length=250,null=True,blank=True)
    phone=models.CharField(max_length=15,null=True,blank=True)
    city=models.CharField(max_length=30,null=True,blank=True)
    zipcode=models.CharField(max_length=10,null=True,blank=True)

