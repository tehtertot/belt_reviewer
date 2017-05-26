from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^addBook$', views.addBook, name="add"),
    url(r'^viewBook/(?P<id>\d*)$', views.viewBook, name="book"),
    url(r'^add/(?P<id>\d*)$', views.addReview, name="addReview"),
    url(r'^user/(?P<id>\d*)$', views.viewUser, name="user"),
    url(r'^deleteReview/(?P<id>\d*)$', views.deleteReview, name="deleteReview")
]
