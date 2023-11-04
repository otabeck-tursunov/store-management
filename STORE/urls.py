from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Store Management API Documentation",
        default_version="v1",
        description="Admin panel - /admin/ linkida \n"
                    "login: admin, password: 123\n\n"
                    "Xodim useri uchun: \n"
                    "username: akmaljon, password: Otabek06/",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="tursunovotabekkuva@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('userApp.urls')),
    path('main/', include('mainApp.urls')),
    path('cash/', include('cashApp.urls')),
    path('stats/', include('statsApp.urls')),
    path('', schema_view.with_ui('swagger', cache_timeout=0)),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
