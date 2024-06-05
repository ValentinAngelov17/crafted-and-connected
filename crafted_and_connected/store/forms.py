from django import forms
from .models import CartItem


class AddToCartForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']


class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=100, label='Име')
    last_name = forms.CharField(max_length=100, label='Фамилия')
    email = forms.EmailField(max_length=100, label='Email')
    phone_number = forms.CharField(max_length=10, min_length=10, label='Телефонен номер')
    billing_address = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 30}), label='Адрес за доставка')

