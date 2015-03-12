from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'redlibros.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^registro/$', views.registro, name="registro"),
    url(r'^login/$', views.login, name="login"),
    url(r'^mi_perfil/$', views.perfil_propio, name="perfil_propio"),
    url(r'^(?P<username>\w+)/$', views.perfil_usuario, name="perfil_usuario")
)