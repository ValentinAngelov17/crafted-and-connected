from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import PasswordInput
from .models import CustomUser


class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'password ele', 'placeholder': 'Парола'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'email ele', 'placeholder': 'Имейл'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'name ele', 'placeholder': 'Име'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'name ele', 'placeholder': 'Фамилия'}))

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password']


class CustomUserLoginForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'email ele', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'password ele', 'placeholder': 'Password'}))

    class Meta:
        fields = ['email', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['username']
