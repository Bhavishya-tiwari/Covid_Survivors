from django.urls import path,include
from blog import views

urlpatterns = [
    path('', views.blogHome, name='blogHome'),
    path('<int:mysno>', views.blogPost, name='blogPost'),
    path('addblog', views.addblog, name='addblog'),
    path("delB/<int:dsno>", views.delblog, name='delblog'),
    path("repblog/<int:rsno>", views.repblog, name='repblog'),
]