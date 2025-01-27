from rest_framework import viewsets, mixins

from station.models import Bus
from station.serializers import BusSerializers


class BusListView(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin
):
    queryset = Bus.objects.all()
    serializer_class = BusSerializers
