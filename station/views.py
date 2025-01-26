from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from station.models import Bus
from station.serializers import BusSerializers


@api_view(["GET", "POST"])
def bus_list(request):
    if request.method == "GET":
        buses = Bus.objects.all()
        serializer = BusSerializers(buses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        serializer = BusSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def bus_detail(request, pk):
    bus = get_object_or_404(Bus, pk=pk)
    if request.method == "GET":
        serializer = BusSerializers(bus)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        serializer = BusSerializers(bus, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        bus.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
