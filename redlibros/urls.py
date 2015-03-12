from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',    
    url(r'^libros/', include('libros.urls', namespace="libros")),
    url(r'^perfil/', include('perfiles.urls', namespace="perfiles")),
    url(r'^admin/', include(admin.site.urls))
)