from . import views
from django.urls import path
from .dash_apps.finsh_app import simple_example, table, raw_table, bubble_chart

urlpatterns = [
    path(r'', views.home, name='home'),
    # path(r'maps/', views.maps, name='maps'),
    path(r'show_table/', views.show_table, name='show_table'),
    # path(r'test/', views.test, name='test')

]
