# -*- coding: utf-8 -*-

from django import forms
from django.forms import TextInput, URLInput, Textarea, CheckboxInput, HiddenInput, Select

from models import BibliotecaCompartida


class FormNuevoLibro(forms.Form):

	titulo = forms.CharField(max_length=255, required=True, widget=TextInput(attrs={'class': 'form-control'}))
	autor = forms.CharField(max_length=255, required=True, widget=TextInput(attrs={'class': 'form-control'}))	
	descripcion = forms.CharField(max_length=2500, required=False, widget=Textarea(attrs={'class': 'form-control', 
	'placeholder': 'Edición, traductor, un link a Amazon que muestre la versión del libro que tienes, el estado del libro o cualquier información extra que desees compartir.'}))
	disponible = forms.BooleanField(initial=True, help_text="Este libro estará listo para ser prestado", widget=CheckboxInput())


class FormPedirLibro(forms.Form):

	libro_id = forms.IntegerField(required=False, widget=HiddenInput())
	mensaje = forms.CharField(max_length=500, required=False, widget=Textarea(attrs={'class': 'form-control', 'placeholder': 'Hola ...'}))
	telefono = forms.CharField(required=False, widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Importante. Para que pueda contactarte.'}))
	email = forms.CharField(max_length=500, required=False, widget=TextInput(attrs={'class': 'form-control'}))


class NuevaBibliotecaCompartida(forms.ModelForm):
	
	class Meta:
		model = BibliotecaCompartida
		fields = ('nombre', 'direccion', 'imagen')

		widgets = {
					'nombre': TextInput(attrs={'class': 'form-control'}),
					'direccion': Textarea(attrs={'class': 'form-control'}),
					'imagen': URLInput(attrs={'class': 'form-control'})
				}


class EditarBibliotecaCompartida(NuevaBibliotecaCompartida):

	pass


class FormPrestarLibroBCompartida(forms.Form):

	_choices = [("2_semanas", "2 Semanas"), ('1_mes', '1 Mes'), ('2_meses', '2 Meses'), ('3_meses', '3 Meses'), ('indefinido', 'Sin fecha máxima')]

	usuario = forms.CharField(max_length=255, required=True)
	tiempo_entrega = forms.ChoiceField(choices=_choices, required=False, initial=_choices[2][0], widget=Select())
