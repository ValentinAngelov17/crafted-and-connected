from crafted_and_connected.social.models import Notification


def create_order_status_notification(order):
    # Assuming you have a Notification model and a way to create notifications
    Notification.objects.create(
        recipient=order.user,
        content=f"Your order #{order.id} has been {order.status}.",
        order=order
    )
