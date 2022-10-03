"""LibraryManagementSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from library.views import LoginAPI, RegisterAPI, home, signin, signout, book_list, getbook, edit, addbook, delete, book_details
from rest_framework.urlpatterns import format_suffix_patterns
from knox import views as knox_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/books/', book_list, name='books'),
    path('api/books/<int:id>', book_details),
    path('', home, name='home'),
    path('addbook/', addbook, name='addbook'),
    path('getbook/', getbook, name='getbook'),
    path('edit/<int:pk>/', edit, name='edit'),
    path('delete/<int:pk>/', delete, name='delete'), 
    path('login/', signin, name='login'),
    path('logout/', signout, name='logout'), 
]   
urlpatterns=format_suffix_patterns(urlpatterns)