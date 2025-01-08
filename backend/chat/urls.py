from django.urls import path
from .views import chatPage

urlpatterns = [
    path('chat/<str:user>/', chatPage)
]