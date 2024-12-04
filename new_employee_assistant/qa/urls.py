from django.urls import path
from .views import ai_response_view

urlpatterns = [
    path("ai-response/", ai_response_view, name="ai_response"),
]