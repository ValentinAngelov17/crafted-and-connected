from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from crafted_and_connected.store.utils import create_order_status_notification

User = get_user_model()


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
    post = models.ForeignKey('social.Post', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.post.title} ({self.quantity})"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', _('В изчакване')),
        ('accepted', _('Приета')),
        ('declined', _('Отказана')),
        ('sent_to_delivery', _('Изпратена за получаване')),
        ('delivered', _('Получена'))
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='seller_orders', on_delete=models.CASCADE,
                               null=True, blank=True)
    items = models.TextField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_option = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    billing_address = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user}"

    def save(self, *args, **kwargs):
        if self.pk is not None:
            orig = Order.objects.get(pk=self.pk)
            if orig.status != self.status:
                create_order_status_notification(self)
        super().save(*args, **kwargs)
