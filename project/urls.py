from django.conf.urls import url

from minimal import views

urlpatterns = [
    url(r'^$', views.index),
]
