from django.urls import path
from . import views

urlpatterns = [
    path('<str:test_name>/', views.GenericTestPage),
    path('<str:test_name>/run/', views.GenericTestRun),
    path('<str:test_name>/results/', views.GenericTestResults),
]
