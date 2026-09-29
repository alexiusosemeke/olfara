from django.urls import path, include

from rest_framework.routers import DefaultRouter
from accounts.views import UserViewSet

router = DefaultRouter()

router.register("users", viewset=UserViewSet, basename="user")


urlpatterns = [
    path("", include(router.urls)),
    path(
        "auth/register/",
        view=
    ),
]
