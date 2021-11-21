# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('users', views.UserListView)

urlpatterns = [
    path('', include(router.urls), name='api'),
    #path('users/', views.UserListView.as_view()),
    #path('users/<int:pk>/', views.UserView.as_view()),
]

