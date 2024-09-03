from django.db import models

from apps.users.models import User


class City(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'
        ordering = ['-created']

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['-created']

    def __str__(self):
        return self.name


class Product(models.Model):
    price = models.FloatField(default=0)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    # TODO
    # images = ...
    categories = models.ManyToManyField(Category, related_name='product_categories')
    cities = models.ManyToManyField(City, related_name='product_cities')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-created']

    def __str__(self):
        return self.title


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    rating = models.IntegerField(default=0)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ['-created']

    def __str__(self):
        return f'{self.product} - {self.user} - {self.rating} - {self.description}'


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    text = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'
        ordering = ['-created']


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-created']

    def __str__(self):
        return f'{self.user}'


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1)
    price = models.FloatField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Order item'
        verbose_name_plural = 'Order items'
        ordering = ['-created']

    def __str__(self):
        return f'{self.user} - {self.order}'
