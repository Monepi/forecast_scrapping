from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.show_index, name='show_index'),
    url(r'^login$', views.show_login, name='show_login'),
    url(r'^register$', views.show_register, name='show_register'),
    url(r'^weather$', views.show_weather, name='show_weather'),
    url(r'^api_forecast$', views.get_api_weather),
    url(r'^api/(?P<username>\w+)/(?P<password>\w+)$', views.api_weather),
    url(r'^logout$', views.logout, name='logout')
]
