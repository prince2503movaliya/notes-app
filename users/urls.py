from django.urls import path
from users.api_views import CustomTokenView
from .views import register_view, login_view, logout_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('api/token/', CustomTokenView.as_view(), name='token'),
]



