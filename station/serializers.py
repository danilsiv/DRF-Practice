from rest_framework import serializers
from station.models import Bus


class BusSerializers(serializers.ModelSerializer):

    class Meta:
        model = Bus
        fields = ("id", "info", "num_seats", "is_small")
