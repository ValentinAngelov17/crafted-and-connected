from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Like, Notification
from .forms import PostForm, CommentForm
from ..authentication.models import Follow


@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            # Notify followers about the new post
            followers = Follow.objects.filter(followed=request.user)
            for follower_relation in followers:
                follower = follower_relation.follower
                Notification.objects.create(
                    recipient=follower,
                    content=f"User {request.user.first_name} {request.user.last_name} added a new post '{post.title}'",
                    post=post
                )

            return redirect('profile')
    else:
        form = PostForm()
    return render(request, 'add_post.html', {'form': form})


def load_subcategories(request):
    category = request.GET.get('category')
    subcategories = Post.SUBCATEGORY_CHOICES.get(category, [])
    return JsonResponse([{'value': subcategory[0], 'display': subcategory[1]} for subcategory in subcategories],
                        safe=False)


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    is_liked = post.likes.filter(id=request.user.id).exists()

    is_following_post_user = Follow.objects.filter(follower=request.user, followed=post.user).exists()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', post=post)
    else:
        form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'is_liked': is_liked,
        'form': form,
        'is_following_post_user': is_following_post_user,  # Include the variable in the context
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


@login_required
def notifications(request):
    user = request.user
    notifications = Notification.objects.filter(recipient=user).order_by('-timestamp')
    return render(request, 'notifications.html', {'notifications': notifications})


@login_required
def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.read = True
    notification.save()
    return redirect('notifications')


def create_order_status_notification(order):
    content = f"Order #{order.id} status has changed to {order.get_status_display()}."
    recipient = order.user  # Assuming the order has a 'user' field that links to the User model
    Notification.objects.create(recipient=recipient, content=content, order=order)


@login_required
def clear_notifications(request):
    user = request.user
    Notification.objects.filter(recipient=user).delete()
    return redirect('notifications')
