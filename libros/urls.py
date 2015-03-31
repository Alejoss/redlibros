from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^main/$', views.main, name="main"),
    url(r'^nuevo_libro/$', views.nuevo_libro, name="nuevo_libro"),
    url(r'^mi_biblioteca/$', views.mi_biblioteca, name="mi_biblioteca"),
    url(r'^ciudad/(?P<slug_ciudad>\w+)/(?P<id_ciudad>\d+)/$', views.libros_ciudad, name="libros_ciudad"),
    url(r'^libro/(?P<slug_libro>\w+)/(?P<id_libro>\d+)/$', views.libro, name="libro"),
    url(r'^libro/(?P<username>\w+)/$', views.libros_usuario, name="libros_usuario"),

    url(r'^pedirlibro/(?P<id_libro>\d+)/$', views.pedir_libro, name="pedir_libro")
)
