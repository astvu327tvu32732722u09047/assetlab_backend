from django.urls import path
from .views import RegisterView, LoginView, AiAnalysisView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('analyze/', AiAnalysisView.as_view(), name='analyze'),
]
