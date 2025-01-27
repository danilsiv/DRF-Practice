from django.db import models


class Bus(models.Model):
    info = models.CharField(max_length=255, null=True)
    num_seats = models.IntegerField()
    facilities = models.ManyToManyField

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
