from django.urls import path, include
from rest_framework import routers

from station.views import (
    BusViewSet,
    TripViewSet,
)

router = routers.DefaultRouter()
router.register("buses", BusViewSet)
router.register("trips", TripViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "station"
