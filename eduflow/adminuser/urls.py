from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('course', views.CourseAdminView, basename='course')
router.register('course/<int:pk>/', views.CourseAdminView, basename='coursedetail')
router.register('subject', views.SubjectAdminView, basename='subject')
router.register('chapter', views.ChapterAdminView, basename='chapter')
router.register('lesson', views.LessonAdminView, basename='lesson')

urlpatterns = [
    path('userlist/',views.UsersListAdminView.as_view()),
    path('student/',views.StudentLsistAdminview.as_view()),
    path('teacher/',views.TeacherListAdminView.as_view()),
    # path('',views.abc.as_view()),

    path('study/', include(router.urls))
]


from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



