from django.urls import path

from . import views

urlpatterns = [
    path('oauth/', views.index, name='index'),
    path('complete/', views.complete, name='index'),


]
