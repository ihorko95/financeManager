from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.datetime_safe import datetime

from goods.models import *


class GoodsForm(forms.ModelForm):
    class Meta:
        model = Goods
        fields = ['title','slug','body','cat','quantity','price','is_required']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.TextInput(attrs={'class': 'form-control'}),
            'cat': forms.Select(attrs={'class': 'form-select'}, ),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_required': forms.CheckboxInput(attrs={'class': 'form-check-label'}),

        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name','slug','body']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.TextInput(attrs={'class': 'form-control'}),
        }

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="User Name:*", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=False, label="Email:", widget=forms.EmailInput(attrs={'class': 'form-control', 'requered':'false'}))
    first_name = forms.CharField(required=False, label="First Name:", widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=False, label="Last Name:", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="Password:*",widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Confirm password:*", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        # widgets = {
        #    'username': forms.TextInput(attrs={'class': 'form-control'}),
        #    'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
        #    'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        # }
class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="User Name:", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password:", widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class ReportForm(forms.Form):
    time_from = forms.DateTimeField(label="From:", widget=forms.DateInput(
        attrs={'class': 'form-control', 'type': 'date'}),
        initial=format('%Y-%m-%dT%H:%M'))
    time_to = forms.DateTimeField(label="To:", widget=forms.DateInput(
        attrs={'class': 'form-control', 'type': 'date'}),
        initial=format('%Y-%m-%dT%H:%M'))

    operation = forms.ModelChoiceField(queryset=Category.objects.all(),
                                       widget=forms.Select(attrs={'class': 'form-select'}),
                                       empty_label="All",
                                       required=False
                                       )
