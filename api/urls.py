from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import UserRegisterView, UserLoginView, UserProfileView, UserView, BookingViewSet, PaymentViewSet


schema_view = get_schema_view(
    openapi.Info(
        title="EV Charging Locator API",
        default_version='v1',
        description="EV Charging Locator API",
        terms_of_service="",
        contact=openapi.Contact(email=""),
        license=openapi.License(name=""),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)
urlpatterns = [
    path('swagger<str:format>', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('user/', UserView.as_view(), name='user'),
    path('bookings/', BookingViewSet.as_view({'post': 'create', 'get': 'list'}), name='bookings-list'),
    path('bookings/<int:pk>/', BookingViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='bookings-detail'),
    path('payment/', PaymentViewSet.as_view({'post': 'create'}), name='payment-create'),
]
    
   
