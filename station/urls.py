from django.urls import path
from station.views import BusListView, BusDetailView

urlpatterns = [
    path("buses/", BusListView.as_view(), name="bus_list"),
    path("buses/<int:pk>/", BusDetailView.as_view(), name="bus_detail"),
]

app_name = "station"
