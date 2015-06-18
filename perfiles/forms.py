# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from models import Perfil


class formRegistro(UserCreationForm):

	username = forms.RegexField(label=("Username"), max_length=30,
        regex=r'^[\w.@+-]+$',        
        error_messages={
            'invalid': ("This value may contain only letters, numbers and " "@/./+/-/_ characters.")},
            widget=forms.TextInput(attrs={'class': 'form-control'})
            )

	password1 = forms.CharField(label=("Password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

	password2 = forms.CharField(label=("Password confirmation"),
                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

	class Meta:
		model = User
		fields = ("first_name", "last_name", "email", "username", "password1", "password2")
		widgets = {
				'first_name': forms.TextInput(attrs={'class': 'form-control'}),
				'last_name': forms.TextInput(attrs={'class': 'form-control'}),
				'email': forms.TextInput(attrs={'class': 'form-control'})
		}


class formEditarPerfil(forms.ModelForm):

	class Meta:
		model = Perfil
		fields = ("descripcion", "ciudad", "numero_telefono_contacto")
		widgets = {
				'descripcion': forms.Textarea(attrs={'class': 'form-control', 
				'placeholder': 'Tus intereses literarios. El sector de la ciudad en que vives para facilitar los futuros intercambios...'}),
				'ciudad': forms.Select(attrs={'class': 'form-control'}),
				'numero_telefono_contacto': forms.TextInput(attrs={'class': 'form-control'})
		}
