from django.urls import path
from . import views

urlpatterns = [
  path('contactus/', views.MessagesView.as_view()),
]