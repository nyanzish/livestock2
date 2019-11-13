
from django.conf import settings
from django.db import models
from django.shortcuts import reverse


# Create your models here.


CATEGORY_CHOICES = (
    ('Cows', 'Cows'),
    ('Chicken', 'Chicken'),
    ('Ducks', 'Ducks'),
    ('Goats', 'Goats')
)


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    discount_price = models.IntegerField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=10)
    #label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField()
    image = models.FileField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("shop:product", args=[str(self.pk)
        ])

    def get_add_to_cart_url(self):
        return reverse("shop:add_to_cart", args=[str(self.pk)])

    def get_remove_from_cart_url(self):
        return reverse("shop:remove_from_cart", args=[str(self.pk)])

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


    def __str__(self):
        return f'{self.quantity} of {self.item.title}'

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem )
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total


class Farmer(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length = 200)
    email = models.EmailField(default = None)
    farmname = models.CharField(max_length = 50)
    farmlocation = models.CharField(max_length = 100)
    phone = models.CharField(max_length = 10)
    

    def __str__(self):
        return self.farmname