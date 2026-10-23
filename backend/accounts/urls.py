from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from accounts.views import UserViewSet, RegisterUserView

router = DefaultRouter()

router.register("users", viewset=UserViewSet, basename="user")


urlpatterns = [
    path("", include(router.urls)),
    path("auth/login/", view=TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/refresh/", view=TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/register/", view=RegisterUserView.as_view(), name="register"),
]
