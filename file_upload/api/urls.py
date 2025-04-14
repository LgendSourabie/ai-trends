from django.urls import path
from file_upload.api import views

urlpatterns = [
    path('file/', views.fileView.as_view()),
]
