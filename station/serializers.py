from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from station.models import Bus, Trip, Facility, Ticket, Order


class FacilitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Facility
        fields = ("id", "name")


class BusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bus
        fields = ("id", "info", "num_seats", "is_small", "facilities")


class BusListSerializer(BusSerializer):
    facilities = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )


class BusRetrieveSerializer(BusSerializer):
    facilities = FacilitySerializer(many=True)


class TripSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trip
        fields = ("id", "source", "destination", "departure", "bus")


class TripListSerializer(serializers.ModelSerializer):
    bus_info = serializers.CharField(source="bus.info", read_only=True)
    bus_num_seats = serializers.IntegerField(source="bus.num_seats", read_only=True)
    tickets_available = serializers.IntegerField(read_only=True, source="available_tickets")

    class Meta:
        model = Trip
        fields = (
            "id",
            "source",
            "destination",
            "departure",
            "bus_info",
            "bus_num_seats",
            "tickets_available"
        )



class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = ("id", "seat", "trip")
        validators = [
            UniqueTogetherValidator(
                queryset=Ticket.objects.all(),
                fields=["seat", "trip"]
            )
        ]

    def validate(self, attrs) -> None:
        Ticket.validate_seat(attrs["seat"], attrs["trip"].bus.num_seats, ValidationError)


class TripRetrieveSerializer(serializers.ModelSerializer):
    bus = BusRetrieveSerializer(read_only=True, many=False)
    taken_seats = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="seat",
        source="tickets"
    )

    class Meta:
        model = Trip
        fields = ("id", "source", "destination", "departure", "bus", "taken_seats")


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Order
        fields = ("id", "created_at", "tickets")

    def create(self, validated_data) -> Order:
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets", None)
            order = Order.objects.create(**validated_data)
            for ticket in tickets_data:
                Ticket.objects.create(order=order, **ticket)
            return order


class TicketListSerializer(TicketSerializer):
    trip = TripListSerializer(read_only=True)


class OrderListSerializer(OrderSerializer):
    tickets = TicketListSerializer(read_only=True, many=True)
