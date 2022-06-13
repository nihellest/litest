from django.urls import path
from . import views

urlpatterns = [
    path('<str:test_name>/', views.generic_test_page),
    path('<str:test_name>/run/', views.generic_test_run),
    path('<str:test_name>/results/', views.generic_test_results),
]
