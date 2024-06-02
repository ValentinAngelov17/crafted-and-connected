from django.db import models
from django.conf import settings

from crafted_and_connected.social.models import Post


# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return f"Cart of {self.user}"

    def get_total_price(self):
        total = sum(item.post.price * item.quantity for item in self.items.all())
        print(f"Calculating total price for cart {self.id}: {total}")
        return total


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.post.title} ({self.quantity})"
