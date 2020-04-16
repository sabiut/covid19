from . import views
from django.urls import path

urlpatterns = [
    path(r'', views.home, name='home'),

]