# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class formRegistro(UserCreationForm):

	class Meta:
		model = User
		fields = ("first_name", "last_name", "email", "username", "password1", "password2")
		widgets = {
				'first_name': forms.TextInput(attrs={'class':'form-control'}),
				'last_name': forms.TextInput(attrs={'class':'form-control'}),
				'email': forms.TextInput(attrs={'class':'form-control'}),
				'username': forms.TextInput(attrs={'class':'form-control'}),
				'password1': forms.PasswordInput(attrs={'class':'form-control'}),
				'password2': forms.PasswordInput(attrs={'class':'form-control'})
		}