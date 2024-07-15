from django.urls import path

from . import views

urlpatterns = [
  path('recipe/', views.DbmoduleView.as_view()),
  path('recipe/<int:id>/', views.DbmoduleView.as_view()),
]