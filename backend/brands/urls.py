from django.urls import path

from .views import BrandViewSet

urlpatterns = [path("brand/", view=BrandViewSet.as_view(), name="brand")]
