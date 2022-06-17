from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_page),
    path('login/', views.login_page),
    path('logout/', views.logout_page),
    path('profile/', views.profile_page),
]