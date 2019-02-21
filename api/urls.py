from django.urls import path

# Class Imports
from api.views.Authentication import ListUser, RegistrationAPIView, GenerateOTPView, UserLoginView
from api.views.Service import TabList

urlpatterns = [
    # authentication apts
    path('user/list', ListUser.as_view()),
    path('user/register/', RegistrationAPIView.as_view()),
    path('user/login/', UserLoginView.as_view()),
    path('user/gen/otp/', GenerateOTPView.as_view()),
    # service apis
    path('service/tab/list', TabList.as_view()),
]