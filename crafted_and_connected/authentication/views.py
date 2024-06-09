from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.views.generic import CreateView
from crafted_and_connected.authentication.forms import CustomUserCreationForm, CustomUserLoginForm, \
    CustomPasswordChangeForm, ProfileForm
from crafted_and_connected.authentication.models import Follow, CustomUser
from django.contrib.auth.hashers import make_password
from crafted_and_connected.social.models import Post
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
User = get_user_model()


# Create your views here.
class CustomUserRegistrationView(CreateView):
    template_name = 'register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        # Hash the password before saving
        form.instance.password = make_password(form.cleaned_data['password'])
        return super().form_valid(form)


class CustomLoginView(LoginView):
    authentication_form = CustomUserLoginForm
    template_name = 'login.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.pop('request', None)  # Remove the 'request' argument
        return kwargs

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')

        # Authenticate user using the custom authentication backend
        user = authenticate(request=self.request, email=email, password=password,
                            backend='crafted_and_connected.authentication.backends.EmailModelBackend')

        if user is not None:
            # Authentication successful
            login(self.request, user)
            return HttpResponseRedirect(self.get_success_url())
        else:
            # Authentication failed
            return self.form_invalid(form)


@login_required
def profile(request):
    user = request.user
    return redirect('user_profile', user_id=user.id)


@login_required
def logout_view(request):
    logout(request)
    return redirect('index')


@login_required
def update_profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user)
        password_form = CustomPasswordChangeForm(user=request.user, data=request.POST)

        if profile_form.is_valid():
            user = profile_form.save(commit=False)
            if password_form.is_valid():
                new_password = password_form.cleaned_data.get('new_password1')
                if new_password:
                    user.set_password(new_password)
                user.save()

                if new_password:
                    update_session_auth_hash(request, user)  # Update the session with the new password

                messages.success(request, 'Your profile has been updated successfully.')
                return redirect('profile')  # Redirect to profile page after successful update
            else:
                for error in password_form.errors.values():
                    messages.error(request, error)
        else:
            for error in profile_form.errors.values():
                messages.error(request, error)

    else:
        profile_form = ProfileForm(instance=request.user)
        password_form = CustomPasswordChangeForm(user=request.user)

    return render(request, 'update_profile.html', {
        'profile_form': profile_form,
        'password_form': password_form,
    })

@login_required
def user_profile(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    room_name = f"user_{request.user.id}_to_{user_id}"
    print("Room name:", room_name)
    posts = Post.objects.filter(user=user).order_by('-created_at')
    post_count = posts.count()
    followers_count = Follow.objects.filter(followed=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    is_following = Follow.objects.filter(follower=request.user, followed=user).exists()
    return render(request, 'profile.html', {
        'user': user,
        'followers_count': followers_count,
        'following_count': following_count,
        'posts': posts,
        'post_count': post_count,
        'is_following': is_following,
        'room_name': room_name,
    })


@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(CustomUser, id=user_id)
    follow, created = Follow.objects.get_or_create(follower=request.user, followed=user_to_follow)
    return redirect(reverse('user_profile', args=[user_id]))


@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(CustomUser, id=user_id)
    Follow.objects.filter(follower=request.user, followed=user_to_unfollow).delete()
    return redirect(reverse('user_profile', args=[user_id]))
