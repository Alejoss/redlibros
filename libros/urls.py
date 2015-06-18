from django.conf.urls import url
import views

urlpatterns = [    
    url(r'^main/$', views.main, name="main"),
    url(r'^nuevo_libro/(?P<tipo_dueno>\w+)/(?P<username>[-\w.]+)/$', views.nuevo_libro, name="nuevo_libro"),
    url(r'^mi_biblioteca/$', views.mi_biblioteca, name="mi_biblioteca"),
    url(r'^ciudad/(?P<slug_ciudad>\w+)/(?P<id_ciudad>\d+)/(?P<filtro>\w+)/$', views.libros_ciudad, name="libros_ciudad"),    
    url(r'^buscar_ciudad/$', views.buscar_ciudad, name="buscar_ciudad"),

    url(r'^libro/(?P<slug_libro>\w+)/(?P<id_libro>\d+)/$', views.libro, name="libro"),
    url(r'^libro/(?P<username>[-\w.]+)/$', views.libros_usuario, name="libros_usuario"),

    url(r'^pedirlibro/(?P<id_libro_disponible>\d+)/$', views.pedir_libro, name="pedir_libro"),
    url(r'^libro_request/(?P<libro_request_id>\d+)/$', views.libro_request, name="libro_request"),

    url(r'^prestar_libro/(?P<libro_request_id>\d+)/$', views.prestar_libro, name="prestar_libro"),
    
    url(r'^biblioteca_compartida/(?P<slug_biblioteca_compartida>[-\w]+)/$', views.biblioteca_compartida, name="biblioteca_compartida"),

    url(r'^nueva_biblioteca_compartida/(?P<slug_ciudad>\w+)/(?P<id_ciudad>\d+)/$', views.nueva_biblioteca_compartida, 
        name="nueva_biblioteca_compartida"),
    url(r'^editar_info_bcompartida/(?P<slug_biblioteca_compartida>[-\w]+)/$', views.editar_info_bcompartida, 
        name="editar_info_bcompartida"),
    url(r'^editar_libros_bcompartida/(?P<slug_biblioteca_compartida>[-\w]+)/$', views.editar_libros_bcompartida, 
        name="editar_libros_bcompartida"),
    url(r'^prestar_libro_biblioteca_compartida/(?P<id_libro_compartido>\d+)/$', views.prestar_libro_bcompartida, 
        name="prestar_libro_bcompartida"),

    url(r'^anunciar_devolucion/$', views.anunciar_devolucion, 
        name="anunciar_devolucion"),
    url(r'^cancelar_pedido/$', views.cancelar_pedido, 
        name="cancelar_pedido"),

    url(r'^buscar/(?P<slug_ciudad>\w+)/(?P<filtro>\w+)/$', views.buscar, name='buscar'),

    url(r'^cambiar_dueno_libros/$', views.cambiar_dueno_libros, name="cambiar_dueno_libros"),
    
    # Ajax calls
    url(r'^marcar_no_disponible/$', views.marcar_no_disponible),
    url(r'^marcar_disponible/$', views.marcar_disponible),
    url(r'^marcar_devuelto/$', views.marcar_devuelto)
]
