from . import views
from django.urls import path
from .dash_apps.finsh_app import simple_example, table

urlpatterns = [
    path(r'', views.home, name='home'),
    path(r'maps/', views.maps, name='maps')

]
