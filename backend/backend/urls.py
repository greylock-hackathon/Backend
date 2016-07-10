from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^twilio/new_message', views.new_message),
    url(r'^uber/redirect', views.redirect),
    url(r'^uber/poll/$', views.uber_poll),
    url(r'^uber/update/$', views.uber_update),
    url(r'^admin/', admin.site.urls),
]
