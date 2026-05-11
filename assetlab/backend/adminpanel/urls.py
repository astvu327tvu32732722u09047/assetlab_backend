from django.urls import path
from .views import AdminRegisterView, AdminLoginView

urlpatterns = [
    path('register/', AdminRegisterView.as_view()),
    path('login/', AdminLoginView.as_view()),
]
