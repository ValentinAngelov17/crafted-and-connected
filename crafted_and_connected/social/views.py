from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Like, SUBCATEGORY_CHOICES
from .forms import PostForm, CommentForm


@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('profile')
    else:
        form = PostForm()
    return render(request, 'add_post.html', {'form': form})


def load_subcategories(request):
    category = request.GET.get('category')
    print(f"Category received: {category}")
    subcategories = SUBCATEGORY_CHOICES.get(category, [])
    print(f"Subcategories returned: {subcategories}")
    return JsonResponse([{'value': subcategory[0], 'display': subcategory[1]} for subcategory in subcategories],
                        safe=False)


# <!-- TODO:  <a href="{% url 'post_detail' post_id %}"> </a><!-->
@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    is_liked = post.likes.filter(id=request.user.id).exists()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', post_id=post_id)
    else:
        form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'is_liked': is_liked,
        'form': form,
    }
    return render(request, 'post_detail.html', context)


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('post_detail', post_id=post_id)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        text = request.POST.get('text')
        comment = Comment.objects.create(user=request.user, post=post, text=text)
        return redirect('post_detail', post_id=post_id)
