from django.shortcuts import render

from forms import formRegistro

# Create your views here.
def registro(request):
	template = "perfiles/registro.html"

	if request.method == "POST":
		pass
	else:
		form = formRegistro()

	context = {
		'form': form
	}
	
	return render(request, template, context)

def login(request):
	template = "perfiles/login.html"
	return render(request, template)


def perfil_propio(request):
	template = "perfiles/perfil_propio.html"
	datos_perfil = ""
	return render(request, template)


def perfil_usuario(request):
	template = "perfiles/perfil.html"
	datos_perfil = ""
	return render(request, template)
