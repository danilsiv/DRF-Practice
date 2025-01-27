from django.urls import path
from station.views import BusListView

bus_list = BusListView.as_view(actions={"get": "list", "post": "create"})
bus_detail = BusListView.as_view(
    actions = {
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy"
    }
)

urlpatterns = [
    path("buses/", bus_list, name="bus_list"),
    path("buses/<int:pk>/", bus_detail, name="bus_detail"),
]

app_name = "station"
