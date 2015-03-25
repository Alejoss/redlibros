from django.shortcuts import render
from django.http import HttpResponse

from forms import formRegistro


def registro(request):
	template = "perfiles/registro.html"

	if request.method == "POST":
		form = formRegistro(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponse("Usuario Guardado", status=201)
	
	else:		
		form = formRegistro()

	context = {
		'form': form
	}
	
	return render(request, template, context)


def perfil_propio(request):
	template = "perfiles/perfil_propio.html"
	datos_perfil = ""
	return render(request, template)


def perfil_usuario(request):
	template = "perfiles/perfil.html"
	datos_perfil = ""
	return render(request, template)
