from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_GET
from django.urls import reverse
from django.db.models import Q
from crafted_and_connected.social.models import Post
from crafted_and_connected.store.forms import CheckoutForm
from crafted_and_connected.store.models import Cart, CartItem


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
    if cart:
        print(f"Cart ID: {cart.id}, Total: {cart.get_total_price()}")
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
            # Save billing details and proceed to payment or order confirmation
            # Here you can handle the order saving logic
            # e.g., create an Order model instance and save the order details
            # For now, we just redirect to a 'thank you' page or order summary
            return render(request, 'order_summary.html', {
                'cart': cart,
                'delivery_option': delivery_option,
                'billing_details': form.cleaned_data
            })
    else:
        form = CheckoutForm(initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name
        })

    return render(request, 'checkout.html', {'cart': cart, 'form': form})
