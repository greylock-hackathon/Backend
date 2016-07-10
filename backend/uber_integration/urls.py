from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^redirect/', views.redirect, name='redirect'),
    #url(r'sandbox',views.sandbox,name='sandbox'),
    #url(r'authenticate',views.authenticate,name='authenticate'),
    #url(r'authentication_callback',views.authentication_callback,name='authentication_callback'),
]
