from rest_framework import serializers
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

    class Meta:
        model = Trip
        fields = ("id", "source", "destination", "departure", "bus_info", "bus_num_seats")


class TripRetrieveSerializer(TripSerializer):
    bus = BusRetrieveSerializer(read_only=True, many=False)


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = ("id", "seat", "trip")


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ("id", "created_at", "user", "tickets")
