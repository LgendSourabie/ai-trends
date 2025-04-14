from django.urls import path, include
from rest_framework.routers import DefaultRouter
from trend_app.api import views

router = DefaultRouter()
router.register("trends", views.TrendViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
