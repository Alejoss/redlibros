from django.conf.urls import url
from django.contrib.auth import views as auth_views

import views

urlpatterns = [
    url(r'^registro/$', views.registro, name="registro"),
    url(r'^login/$', auth_views.login, {'template_name': 'perfiles/login.html'}, name="login"),
    url(r'^logout/$', views.logout_view, name="logout"),
    url(r'^mi_perfil/$', views.perfil_propio, name="perfil_propio"),
    url(r'^editar_perfil/$', views.editar_perfil, name="editar_perfil"),
    url(r'^(?P<username>[-\w.]+)/$', views.perfil_usuario, name="perfil_usuario")
]
