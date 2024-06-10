from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, RoleViewSet  # Import your viewset
from .views import MyTokenObtainPairView

router = DefaultRouter()
router.register('employees', EmployeeViewSet, basename='employee')  # Register your viewset
router.register(r'roles', RoleViewSet)


schema_view = get_schema_view(
    openapi.Info(
        title="Employee API",
        default_version='v1',
        description="API documentation for the Employee app",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@employee.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', include(router.urls)),  # Include the URLs for your APIs
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),


    
]