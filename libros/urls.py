from django.conf.urls import url
import views

urlpatterns = [
    url(r'^main/$', views.main, name="main"),
    url(r'^nuevo_libro/$', views.nuevo_libro, name="nuevo_libro"),
    url(r'^mi_biblioteca/$', views.mi_biblioteca, name="mi_biblioteca"),
    url(r'^ciudad/(?P<slug_ciudad>\w+)/(?P<id_ciudad>\d+)/$', views.libros_ciudad, name="libros_ciudad"),
    url(r'^libro/(?P<slug_libro>\w+)/(?P<id_libro>\d+)/$', views.libro, name="libro"),
    url(r'^libro/(?P<username>\w+)/$', views.libros_usuario, name="libros_usuario"),

    url(r'^pedirlibro/(?P<id_libro_disponible>\d+)/$', views.pedir_libro, name="pedir_libro"),
    url(r'^libro_request/(?P<libro_request_id>\d+)/$', views.libro_request, name="libro_request"),
    url(r'^prestar_libro/(?P<libro_request_id>\d+)/$', views.prestar_libro, name="prestar_libro")
]
