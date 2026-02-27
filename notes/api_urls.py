from django.urls import path, include
from .api_views import NoteViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('notes', NoteViewSet, basename='notes')

urlpatterns = [
    path('', include(router.urls)),
]