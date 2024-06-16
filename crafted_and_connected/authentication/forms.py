from django import forms
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _


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
        fields = ['first_name', 'last_name', 'email', 'description', 'profile_picture']
        labels = {
            'first_name': _('Име'),
            'last_name': _('Фамилия'),
            'email': _('Електронна поща'),
            'profile_picture': _('Профилна снимка')
        }

    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), label='Описание', required=False)


class CustomPasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, label="Текуща парола", required=False)
    new_password1 = forms.CharField(widget=forms.PasswordInput, label="Нова парола", required=False)
    new_password2 = forms.CharField(widget=forms.PasswordInput, label="Потвърди нова парола", required=False)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if old_password and not self.user.check_password(old_password):
            raise forms.ValidationError("Текуща парола е невалидна")
        return old_password

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if old_password or new_password1 or new_password2:
            if not old_password:
                self.add_error('old_password', "Това поле е задължително")
            if not new_password1:
                self.add_error('new_password1', "Това поле е задължително")
            if not new_password2:
                self.add_error('new_password2', "Това поле е задължително")
            if new_password1 and new_password1 != new_password2:
                raise forms.ValidationError("Новата парола несъвпада")
            validate_password(new_password1, self.user)

        return cleaned_data
