"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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


from django.urls import path
from django.contrib.auth import views as auth_views
from watchlist import views



app_name = 'watchlist'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('movies/', views.movie_list, name='movie_list'),
    path('series/', views.series_list, name='series_list'),
    path('series/<int:pk>/', views.series_detail, name='series_detail'),
    path('movies/<int:pk>/', views.movie_detail, name='movie_detail'),
    path('signup/',views.signup, name='signup'),
    path('add/<int:pk>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('remove/<int:pk>/', views.remove_from_watchlist, name='remove_from_watchlist'),
    path('edit/<int:pk>/',views.edit, name='edit'),
    path('mylist/', views.mylist, name='mylist'),
    path('addMovie/', views.add_movie, name='add_movie'),
    path('addSeries/', views.add_series, name='add_series'),

]
