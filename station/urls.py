from django.urls import path, include
from rest_framework import routers

from station.views import (
    BusViewSet,
    TripViewSet,
    FacilityViewSet,
)

router = routers.DefaultRouter()
router.register("buses", BusViewSet)
router.register("trips", TripViewSet)
router.register("facilities", FacilityViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "station"
