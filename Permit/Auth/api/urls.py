from django.urls import path
from Auth.api.views import get_user


urlpatterns = [
    path('auth/',get_user,name='get_user'),
]
