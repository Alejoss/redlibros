from djagno.shortcuts import render

# Create your views here.
def registro(request):

	if request.method == "POST":
		pass
	else:		
		
	template = "perfiles/registro.html"
	return render(request, template)

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
