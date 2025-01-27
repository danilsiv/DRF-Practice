from rest_framework import viewsets

from station.models import Bus
from station.serializers import BusSerializers


class BusViewSet(viewsets.ModelViewSet):
    queryset = Bus.objects.all()
    serializer_class = BusSerializers
