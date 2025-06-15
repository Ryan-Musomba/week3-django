from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('post/<int:pk>/', views.post_view, name='post'),
    path('search/', views.search, name='search'),
    path('like/<int:pk>/', views.like_post, name='like_post'),
]