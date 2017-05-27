from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^login$', views.login, name="login"),
    url(r'^register$', views.register),
    url(r'^success$', views.success),
    url(r'^logout$', views.logout, name="logout")
]
