from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_GET
from django.urls import reverse
from django.db.models import Q
from crafted_and_connected.social.models import Post, Notification
from crafted_and_connected.store.forms import CheckoutForm
from crafted_and_connected.store.models import Cart, CartItem, Order
from decimal import Decimal
from collections import defaultdict
User = get_user_model()




def index(request):
    categories = Post.CATEGORY_CHOICES
    context = {
        'categories': categories,
    }

    return render(request, 'store/index.html', context)


def register(request):
    if request.method == 'GET':
        return render(request, 'authentication/register.html')


@require_GET
def latest_posts(request, ):
    posts = Post.objects.all().order_by('-created_at')[:20]
    posts_data = [{
        'title': post.title,
        'image_url': post.photos.url,
        'post_url': reverse('post_detail', args=[post.id])
    } for post in posts]
    return JsonResponse(posts_data, safe=False)


def category_view(request, category, subcategory=None):
    if subcategory:
        posts = Post.objects.filter(category=category, subcategory=subcategory)
    else:
        posts = Post.objects.filter(category=category)

    categories = Post.CATEGORY_CHOICES
    subcategories_dict = Post.SUBCATEGORY_CHOICES

    context = {
        'posts': posts,
        'category': category,
        'subcategory': subcategory,
        'categories': categories,
        'subcategories_dict': subcategories_dict,
    }
    return render(request, 'store/category.html', context)


def search(request):
    query = request.GET.get('q')
    results = []

    if query:
        results = Post.objects.filter(
            Q(title__icontains=query)
        )

    return render(request, 'store/search_results.html', {'query': query, 'results': results})


def add_to_cart(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    existing_item = cart.items.filter(post=post).first()
    if existing_item:
        existing_item.quantity += 1
        existing_item.save()
    else:
        CartItem.objects.create(cart=cart, post=post, quantity=1)

    return redirect('view_cart')


@login_required
def view_cart(request):
    cart = Cart.objects.filter(user=request.user).first()

    if request.method == 'POST':
        return redirect('checkout')

    return render(request, 'store/cart.html', {'cart': cart})


@login_required
def increase_quantity(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    item.quantity += 1
    item.save()

    return redirect('view_cart')


@login_required
def decrease_quantity(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect('view_cart')


@login_required
def remove_item(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    item.delete()

    return redirect('view_cart')


@login_required
def checkout(request):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart or not cart.items.all():
        return redirect('view_cart')

    total_sum = Decimal(0)
    total_delivery_sum = Decimal(0)
    items_by_user = defaultdict(list)
    for item in cart.items.all():
        items_by_user[item.post.user].append(item)

    for user, items in items_by_user.items():
        order_items_sum = sum(item.post.price * item.quantity for item in items)
        total_sum += order_items_sum
        total_delivery_sum += Decimal(4.50)
    cart_sum = total_sum
    total_sum += total_delivery_sum

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            delivery_option = request.POST.get('delivery')

            return render(request, 'store/order_summary.html', {
                'cart': cart,
                'total_sum': total_sum,
                'total_delivery_sum': total_delivery_sum,
                'cart_sum': cart_sum,
                'delivery_option': delivery_option,
                'billing_details': form.cleaned_data,
            })
    else:
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
        form = CheckoutForm(initial=initial_data)

    return render(request, 'store/checkout.html',
                  {'cart': cart, 'total_sum': total_sum, 'total_delivery_sum': total_delivery_sum, 'cart_sum': cart_sum,
                   'form': form})


@login_required
def create_order(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            cart = Cart.objects.get(user=request.user)
            items_by_user = defaultdict(list)

            for item in cart.items.all():
                items_by_user[item.post.user].append(item)

            orders = []
            delivery_charge = Decimal('4.50')  # fixed delivery charge

            for user, items in items_by_user.items():
                order_items = ", ".join([f"{item.post.title} (Quantity: {item.quantity})" for item in items])
                total_price = sum(item.post.price * item.quantity for item in items) + delivery_charge
                order = Order.objects.create(
                    user=request.user,
                    seller=user,
                    items=order_items,
                    total_price=total_price,
                    delivery_option=request.POST.get('delivery_option', 'default_option'),
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    phone_number=form.cleaned_data['phone_number'],
                    email=form.cleaned_data['email'],
                    billing_address=form.cleaned_data['billing_address'],
                )
                orders.append(order)

                Notification.objects.create(
                    recipient=user,
                    content=f"{request.user.first_name} {request.user.last_name} поръча от Вас.",
                )

            cart.items.all().delete()

            return render(request, 'store/order_confirmation.html', {'orders': orders})

    return redirect('checkout')


@login_required
def order_history(request):
    filter_type = request.GET.get('filter', 'buying')

    if filter_type == 'selling':
        orders = Order.objects.filter(seller=request.user)
    else:
        orders = Order.objects.filter(user=request.user)

    return render(request, 'store/order_history.html', {'orders': orders, 'filter': filter_type})


@login_required
def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    items = order.items.split('\n')

    if request.method == 'POST' and request.user == order.seller:
        if 'approve' in request.POST:
            order.status = 'Приета'
            order.save()
        elif 'decline' in request.POST:
            order.status = 'Отказана'
            order.save()
        return redirect('order_details', order_id=order.id)

    return render(request, 'store/order_details.html',
                  {'order': order, 'items': items})
