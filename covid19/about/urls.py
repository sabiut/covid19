from . import views
from django.urls import path

urlpatterns = [
    path(r'about/', views.about, name='about'),
    path(r'description/', views.description, name='description'),
    path(r'contact/', views.contact, name='contact'),


]
