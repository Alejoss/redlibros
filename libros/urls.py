from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^main/$', views.main, name="main")
)
