from django.db import models
from django.conf import settings
from crafted_and_connected.social.models import Post
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return f"Cart of {self.user}"

    def get_total_price(self):
        total = sum(item.post.price * item.quantity for item in self.items.all())
        print(f"Calculating total price for cart {self.id}: {total}")
        return total

    def total_price_with_delivery(self):
        total = float(sum(item.post.price * item.quantity for item in self.items.all()))
        total += 4.5
        print(f"Calculating total price for cart {self.id}: {total}")
        return total


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.post.title} ({self.quantity})"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('accepted', _('Accepted')),
        ('declined', _('Declined')),
        ('sent_to_delivery', _('Sent to Delivery Company')),
        ('delivered', _('Delivered'))
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.TextField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_option = models.CharField(max_length=50)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    billing_address = models.TextField()
    order_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.pk}"
