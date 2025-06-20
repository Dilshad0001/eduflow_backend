
from django.contrib import admin
from django.urls import path,include,re_path
from django.conf.urls.static import static
from django.conf import settings
# swagger settup
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
# Swagger Schema View
schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="API Documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@myapi.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/',include('account.urls')),
    path('adminuser/',include('adminuser.urls')),
    path('teacher/',include('teacher.urls')),
    path('student/',include('student.urls')),

    # Swagger URLs
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)






