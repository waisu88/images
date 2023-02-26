from django.urls import path
from . import views

urlpatterns = [
    path('', views.image_list_create_api_view),
    path('<int:pk>/', views.image_detail_api_view),
    path('<int:pk>/thumbnails/', views.thumbnail_list_api_view),
    path('<int:pk>/binary/', views.binary_image_list_create_api_view),
]
