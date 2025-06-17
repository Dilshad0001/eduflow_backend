from django.urls import path,include
from. import views
from rest_framework.routers import DefaultRouter



router = DefaultRouter()
# router.register('submission', views.SubmissionStudentsView, basename='submission')
router.register('profile', views.StudentProfileStudentView, basename='profile')



urlpatterns = [
    path('personal/', include(router.urls)),
    path('lesson/',views.LessonStudentView.as_view()),
    path('task/',views.TaskStudentsView.as_view()),
    path('task/<int:pk>/', views.TaskStudentsView.as_view()),
    path("submission/",views.SubmissionStudentsView.as_view()),
    path('leaderboard/',views.LeaderBoardView.as_view()),
    path('course/',views.StudentCourseView.as_view()),
    path('subject/',views.StudentSubjectView.as_view()),
    path('chapter/',views.StudentChapterView.as_view()),
    path('profile/', views.StudentProfileDetailView.as_view()),

]
