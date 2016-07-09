from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'sandbox',views.sandbox,name='sandbox'),
    url(r'authenticate',views.authenticate,name='authenticate'),
]
