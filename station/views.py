from django.db.models import QuerySet, Count, F
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

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
    BusImageSerializer,
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
        elif self.action == "upload_image":
            serializer = BusImageSerializer

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

    @action(
        methods=["POST"],
        detail=True,
        permission_classes=[IsAdminUser],
        url_path="upload-image"
    )
    def upload_image(self, request, pk=None):
        bus = self.get_object()
        serializer = self.get_serializer(bus, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "facilities",
                type={"type": "array", "items": {"type": "number"}},
                description="Filter by facility id (ex. ?facilities=2,3)",
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        """Get list of buses."""
        return super().list(request, *args, **kwargs)


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


class OrderSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = "page_size"
    max_page_size = 20


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = OrderSetPagination

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
