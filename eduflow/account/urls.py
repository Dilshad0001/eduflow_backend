
from django.urls import path
from . import views

urlpatterns = [

    path('register/',views.register.as_view()),
    path('login/',views.logg.as_view()),
]
