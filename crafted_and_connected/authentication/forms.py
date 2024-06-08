from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.password_validation import validate_password

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


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'profile_picture']


class CustomPasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, label="Old Password", required=False)
    new_password1 = forms.CharField(widget=forms.PasswordInput, label="New Password", required=False)
    new_password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm New Password", required=False)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if old_password and not self.user.check_password(old_password):
            raise forms.ValidationError("Old password is incorrect")
        return old_password

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if old_password or new_password1 or new_password2:
            if not old_password:
                self.add_error('old_password', "This field is required.")
            if not new_password1:
                self.add_error('new_password1', "This field is required.")
            if not new_password2:
                self.add_error('new_password2', "This field is required.")
            if new_password1 and new_password1 != new_password2:
                raise forms.ValidationError("New passwords do not match")
            validate_password(new_password1, self.user)

        return cleaned_data
