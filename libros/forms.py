# -*- coding: utf-8 -*-

from django import forms
from django.forms import TextInput, URLInput, Textarea, CheckboxInput


class FormNuevoLibro(forms.Form):

	titulo = forms.CharField(max_length=255, required=True, widget=TextInput(attrs={'class': 'form-control'}))
	autor = forms.CharField(max_length=255, required=True, widget=TextInput(attrs={'class': 'form-control'}))
	imagen = forms.URLField(max_length=255, required=False, widget=URLInput(attrs={'class': 'form-control'}))
	descripcion = forms.CharField(max_length=2500, required=False, widget=Textarea(attrs={'class': 'form-control'}))
	disponible = forms.BooleanField(initial=True, help_text="Este libro está disponible en tu ciudad", widget=CheckboxInput())
