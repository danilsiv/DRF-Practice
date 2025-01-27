from django.db import models


class Bus(models.Model):
    info = models.CharField(max_length=255, null=True)
    num_seats = models.IntegerField()
    facilities = models.ManyToManyField("Facility", related_name="buses")

    class Meta:
        verbose_name_plural = "buses"

    def __str__(self) -> str:
        return f"Bus: {self.info}"

    @property
    def is_small(self) -> bool:
        return self.num_seats <= 25


class Facility(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "facilities"

    def __str__(self) -> str:
        return self.name


class Trip(models.Model):
    source = models.CharField(max_length=63)
    destination = models.CharField(max_length=63)
    departure = models.DateTimeField()
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name="trip")

    class Meta:
        indexes = [
            models.Index(fields=["source", "destination"]),
            models.Index(fields=["departure"])
        ]

    def __str__(self) -> str:
        return f"{self.source} - {self.destination} ({self.departure})"
