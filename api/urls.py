from django.urls import path

# Class Imports
from api.views import Authentication, Service, Practice, PracticeAssessments, Statistics, ContentUpload

urlpatterns = [
    # authentication apts
    path('auth/user/list', Authentication.ListUser.as_view()),
    path('auth/user/register/', Authentication.RegistrationAPIView.as_view()),
    path('auth/user/login/', Authentication.UserLoginView.as_view()),
    path('auth/user/gen/otp/', Authentication.GenerateOTPView.as_view()),
    path('user/logout/', Authentication.UserLogoutView.as_view()),
    path('user/pushkey/', Authentication.UserPushKeyView.as_view()),
    # service apis
    path('service/tab/list', Service.TabListView.as_view()),
    path('service/subject/list', Service.SubjectListView.as_view()),
    # quiz apis
    path('quiz/initialize/', Practice.QuizInitializeView.as_view()),
    path('quiz/answers/', Practice.QuizAnswersView.as_view()),
    path('quiz/complete/', Practice.QuizCompletionView.as_view()),
    # practice paper list
    path('practice/paper/list', PracticeAssessments.PaperListView.as_view()),
    # statitics
    path('practice/paper/leaderboard/', Statistics.LeaderboardView.as_view()),
    # content-upload
    path('media/upload/', ContentUpload.ContentS3Upload.as_view()),
    path('question/upload/', ContentUpload.QuestionUpload.as_view()),

]