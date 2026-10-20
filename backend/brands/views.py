from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .models import Brand
from .serializers import BrandSerializer

# Create your views here.


class BrandViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]  # noqa: RUF012
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()
