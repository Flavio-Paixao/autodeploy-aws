from django.urls import path
from app import views

urlpatterns = [
    path('', views.dashboard),
    path('login/', views.login_view),
    path('logout/', views.logout_view),
    path('users/', views.manage_users),
    path('api/status/', views.status),
    path('api/endpoints/', views.endpoints),
    path('api/deploys/', views.deploys),
    path('api/deploy/', views.deploy),
]