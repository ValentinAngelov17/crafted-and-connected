from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_GET
from django.urls import reverse
from django.db.models import Q
from crafted_and_connected.social.models import Post
from crafted_and_connected.store.forms import CheckoutForm
from crafted_and_connected.store.models import Cart, CartItem, Order


# Create your views here.
def index(request):
    categories = Post.CATEGORY_CHOICES
    context = {
        'categories': categories,
    }

    return render(request, 'index.html', context)


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')


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
    return render(request, 'category.html', context)


def search(request):
    query = request.GET.get('q')
    results = []

    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    return render(request, 'search_results.html', {'query': query, 'results': results})


def add_to_cart(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    # Check if the item is already in the cart
    existing_item = cart.items.filter(post=post).first()
    if existing_item:
        # If the item is already in the cart, increment the quantity
        existing_item.quantity += 1
        existing_item.save()
    else:
        # If the item is not in the cart, create a new cart item
        CartItem.objects.create(cart=cart, post=post, quantity=1)
    return redirect('view_cart')


@login_required
def view_cart(request):
    cart = Cart.objects.filter(user=request.user).first()

    if request.method == 'POST':
        return redirect('checkout')
    return render(request, 'cart.html', {'cart': cart})


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

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            delivery_option = request.POST.get('delivery')
            return render(request, 'order_summary.html', {
                'cart': cart,
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

    return render(request, 'checkout.html', {'cart': cart, 'form': form})


@login_required
def create_order(request):
    if request.method == 'POST':
        cart = Cart.objects.filter(user=request.user).first()
        if not cart:
            return redirect('view_cart')

        delivery_option = request.POST.get('delivery_option')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        billing_address = request.POST.get('billing_address')

        # Check if all necessary data is available
        if not all([delivery_option, first_name, last_name, phone_number, email, billing_address]):
            return redirect('checkout')  # Redirect back to checkout if any data is missing

        items = ", ".join([f"{item.post.title} (Quantity: {item.quantity})" for item in cart.items.all()])
        total_price = cart.total_price_with_delivery()  # Adding delivery cost

        order = Order.objects.create(
            user=request.user,
            items=items,
            total_price=total_price,
            delivery_option=delivery_option,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
            billing_address=billing_address,
        )

        return render(request, 'order_confirmation.html', {'order': order})

    return redirect('checkout')

