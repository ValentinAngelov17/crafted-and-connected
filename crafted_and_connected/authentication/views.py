from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.views.generic import CreateView, FormView
from crafted_and_connected.authentication.forms import CustomUserCreationForm, CustomUserLoginForm, ProfilePictureForm
from crafted_and_connected.authentication.models import Follow, CustomUser
from django.contrib.auth.hashers import check_password, make_password
from crafted_and_connected.social.models import Post

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
def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    posts = Post.objects.filter(user=user).order_by('-created_at')
    post_count = posts.count()
    followers_count = Follow.objects.filter(followed=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    return render(request, 'profile.html', {
        'user': user,
        'followers_count': followers_count,
        'following_count': following_count,
        'posts': posts,
        'post_count': post_count
    })


@login_required
def logout_view(request):
    logout(request)
    return redirect('index')


# views.py
from django.shortcuts import render, redirect
from .forms import ProfilePictureForm


def update_profile_picture(request):
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to profile page after successful update
    else:
        form = ProfilePictureForm(instance=request.user)
    return render(request, 'update_profile_picture.html', {'form': form})

