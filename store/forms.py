from django.contrib.auth.forms import BaseUserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from .models import Order, Product


class CreateUserForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ["customer", "transaction_id", "status", "complete"]
