from perfiles.models import Perfil


def procesar_perfil(request):
	context = {}
	if request.user.is_authenticated():
		perfil, created = Perfil.objects.get_or_create(usuario=request.user)		
		context['perfil_usuario'] = perfil

	return context
