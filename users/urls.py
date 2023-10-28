from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import *


urlpatterns = [
    path('register/', UserRegister.as_view()),
    path('profile/', Profile.as_view()),
    path('login/', UserLogin.as_view()),
]
