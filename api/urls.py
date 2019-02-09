from django.urls import path

# Class Imports
from api.views.Authentication import ListUser

urlpatterns = [
    path('user/list', ListUser.as_view()),
]