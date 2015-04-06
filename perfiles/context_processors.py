from perfiles.models import Perfil


def procesar_perfil(request):
	context = {}
	if request.user.is_authenticated():
		perfil, created = Perfil.objects.get_or_create(usuario=request.user)		
		context['perfil_usuario'] = perfil

	return context


def procesar_ciudad(request):
	context = {}
	if request.user.is_authenticated():
		perfil, created = Perfil.objects.get_or_create(usuario=request.user)
		if created:
			context['tiene_ciudad'] = False
		else:
			if perfil.ciudad is None:
				context['tiene_ciudad'] = False
			else:
				context['tiene_ciudad'] = True
				context['perfil_ciudad'] = perfil.ciudad

	return context
