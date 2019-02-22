from django.urls import path

# Class Imports
from api.views import Authentication, Service, Practice

urlpatterns = [
    # authentication apts
    path('user/list', Authentication.ListUser.as_view()),
    path('user/register/', Authentication.RegistrationAPIView.as_view()),
    path('user/login/', Authentication.UserLoginView.as_view()),
    path('user/gen/otp/', Authentication.GenerateOTPView.as_view()),
    # service apis
    path('service/tab/list', Service.TabList.as_view()),
    path('service/subject/list', Service.SubjectList.as_view()),
    # quiz apis
    path('quiz/initialize/', Practice.QuizInitialize.as_view()),
]