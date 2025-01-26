from rest_framework import serializers
from station.models import Bus


class BusSerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    info = serializers.CharField(max_length=255, required=False)
    num_seats = serializers.IntegerField(required=True)

    def create(self, validated_data) -> Bus:
        return Bus.objects.create(**validated_data)

    def update(self, instance, validated_data) -> Bus:
        instance.info = validated_data.get("info", instance.info)
        instance.num_seats = validated_data.get("num_seats", instance.num_seats)
        instance.save()

        return instance
