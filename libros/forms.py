# -*- coding: utf-8 -*-

from django import forms
from django.forms import TextInput

from libros.models import Libro


class FormNuevoLibro(forms.ModelForm):

	class Meta:
	 	model = Libro

	 	widgets = {
	 		'titulo': TextInput(attrs={'class': 'form-control'}),
	 		'autor': TextInput(attrs={'class': 'form-control'}),
	 		'imagen': TextInput(attrs={'class': 'form-control'}),
	 		'descripcion': TextInput(attrs={'class': 'form-control'})
	 	}
