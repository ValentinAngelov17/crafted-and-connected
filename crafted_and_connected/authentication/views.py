from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.views.generic import CreateView, FormView
from crafted_and_connected.authentication.forms import CustomUserCreationForm, CustomUserLoginForm
from crafted_and_connected.authentication.models import CustomUser
from django.contrib.auth.hashers import check_password, make_password


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
    return render(request, 'profile.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('index')
