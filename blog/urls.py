from django.urls import path,include
from blog import views

urlpatterns = [
    path('', views.blogHome, name='blogHome'),
    path('blogpost/<str:slug>', views.blogPost, name='blogPost'),
]