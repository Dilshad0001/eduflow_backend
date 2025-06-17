from django.urls import path,include
from. import views
from rest_framework.routers import DefaultRouter



router = DefaultRouter()
router.register('question', views.TaskTeacherView, basename='question')
router.register('lesson', views.LessonTeacherView, basename='lesson')


urlpatterns = [
    path('profile/',views.TeacherPrifileView.as_view()),
    path('submission/',views.SubmissionTeacherView.as_view()),
    path('submission/<int:pk>/',views.SubmissionTeacherView.as_view(), name='submission-update'),
    # path('chapter/',views.ChapterTeacherView.as_view()),
    path('studentlist/',views.UsersListTeacherView.as_view()),
    path('task/', include(router.urls)),
    path('course/',views.CourseTeacherView.as_view()),
    path('subject/',views.TeacherSubjectView.as_view()),
    path('chapter/',views.TeacherChapterView.as_view()),
    

]
