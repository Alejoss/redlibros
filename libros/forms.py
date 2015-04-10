# -*- coding: utf-8 -*-

from django import forms
from django.forms import TextInput, URLInput, Textarea, CheckboxInput, HiddenInput, NumberInput

from models import BibliotecaCompartida


class FormNuevoLibro(forms.Form):

	titulo = forms.CharField(max_length=255, required=True, widget=TextInput(attrs={'class': 'form-control'}))
	autor = forms.CharField(max_length=255, required=True, widget=TextInput(attrs={'class': 'form-control'}))
	imagen = forms.URLField(max_length=255, required=False, widget=URLInput(attrs={'class': 'form-control'}))
	descripcion = forms.CharField(max_length=2500, required=False, widget=Textarea(attrs={'class': 'form-control'}))
	disponible = forms.BooleanField(initial=True, help_text="Este libro está disponible en tu ciudad", widget=CheckboxInput())


class FormPedirLibro(forms.Form):

	libro_id = forms.IntegerField(required=False, widget=HiddenInput())
	mensaje = forms.CharField(max_length=500, required=False, widget=Textarea(attrs={'class': 'form-control'}))
	telefono = forms.IntegerField(required=False, widget=TextInput(attrs={'class': 'form-control'}))
	email = forms.CharField(max_length=500, required=False, widget=TextInput(attrs={'class': 'form-control'}))


class NuevaBibliotecaCompartida(forms.ModelForm):
	
	class Meta:
		model = BibliotecaCompartida
		fields = ['nombre', 'direccion', 'hora_apertura', 'hora_cierre']

		widgets = {
					'nombre': TextInput(attrs={'class': 'form-control'}),
					'direccion': Textarea(attrs={'class': 'form-control'}),
					'hora_apertura': NumberInput(attrs={'class': 'form-control', 'max': '24'}),
					'hora_cierre': NumberInput(attrs={'class': 'form-control', 'max': '24'})
				}
