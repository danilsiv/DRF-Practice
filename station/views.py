from django.db.models import QuerySet, Count, F
from rest_framework import viewsets

from station.models import Bus, Trip, Facility, Order
from station.serializers import (
    BusSerializer,
    TripSerializer,
    TripListSerializer,
    BusListSerializer,
    FacilitySerializer,
    BusRetrieveSerializer,
    TripRetrieveSerializer,
    OrderSerializer,
    OrderListSerializer,
)


class FacilityViewSet(viewsets.ModelViewSet):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer


class BusViewSet(viewsets.ModelViewSet):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer

    @staticmethod
    def _params_to_int(query_string: str) -> list[int]:
        """Converts a string of format '1,2,3' to a list of integers [1, 2, 3]."""
        return [int(str_id) for str_id in query_string.split(",") if str_id.isdigit()]

    def get_serializer_class(self) -> object:
        serializer = self.serializer_class
        if self.action == "list":
            serializer = BusListSerializer
        elif self.action == "retrieve":
            serializer = BusRetrieveSerializer

        return serializer

    def get_queryset(self) -> QuerySet:
        queryset = self.queryset

        facilities = self.request.query_params.get("facilities")
        if facilities:
            facilities = self._params_to_int(facilities)
            queryset = queryset.filter(facilities__id__in=facilities)

        if self.action in ("list", "retrieve"):
            queryset = queryset.prefetch_related("facilities")

        return queryset.distinct()


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

    def get_serializer_class(self) -> object:
        serializer = self.serializer_class
        if self.action == "list":
            serializer = TripListSerializer
        elif self.action == "retrieve":
            serializer = TripRetrieveSerializer

        return serializer

    def get_queryset(self) -> QuerySet:
        queryset = self.queryset
        if self.action == "list":
            queryset = (
                queryset.
                select_related()
                .annotate(available_tickets=F("bus__num_seats") - Count("tickets"))
            )

        if self.action == "retrieve":
            queryset = queryset.select_related()

        return queryset.order_by("id")


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self) -> QuerySet:
        queryset = self.queryset.filter(user=self.request.user)
        if self.action == "list":
            queryset = queryset.prefetch_related("tickets__trip__bus")

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self) -> object:
        serializer = self.serializer_class
        if self.action == "list":
            serializer = OrderListSerializer

        return serializer
