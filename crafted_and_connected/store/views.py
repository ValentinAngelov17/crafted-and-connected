from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.urls import reverse
from django.db.models import Q
from crafted_and_connected.social.models import Post


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
