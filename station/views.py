from rest_framework import generics

from station.models import Bus
from station.serializers import BusSerializers


class BusListView(generics.ListCreateAPIView):
    queryset = Bus.objects.all()
    serializer_class = BusSerializers


class BusDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bus.objects.all()
    serializer_class = BusSerializers
