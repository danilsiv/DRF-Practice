from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from station.models import Bus, Facility
from station.serializers import BusListSerializer, BusRetrieveSerializer

BUS_URL = reverse("station:bus-list")


def sample_bus(**params) -> Bus:
    defaults = {
        "info": "AA 1111 AA",
        "num_seats": 50,
    }
    defaults.update(params)
    return Bus.objects.create(**defaults)


def detail_url(bus_id) -> str:
    return reverse("station:bus-detail", args=(bus_id,))


class UnauthenticatedBusApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self) -> None:
        response = self.client.get(BUS_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBusApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@user.com",
            password="test123user"
        )
        self.client.force_authenticate(self.user)

    def test_bus_list(self) -> None:
        sample_bus()
        bus_with_facilities = sample_bus()
        facility_1 = Facility.objects.create(name="test_1")
        facility_2 = Facility.objects.create(name="test_2")
        bus_with_facilities.facilities.add(facility_1, facility_2)

        response = self.client.get(BUS_URL)
        buses = Bus.objects.all()
        serializer = BusListSerializer(buses, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


    def test_filter_buses_by_facilities(self) -> None:
        bus_without_facilities = sample_bus()
        bus_with_facility_1 = sample_bus(info="AA 0000 AA", num_seats=40)
        bus_with_facility_2 = sample_bus(info="BB 0000 BB", num_seats=60)

        facility_1 = Facility.objects.create(name="test_1")
        facility_2 = Facility.objects.create(name="test_2")

        bus_with_facility_1.facilities.add(facility_1)
        bus_with_facility_2.facilities.add(facility_2)

        response = self.client.get(BUS_URL, {"facilities": f"{facility_1.id},{facility_2.id}"})

        serializer_without_facilities = BusListSerializer(bus_without_facilities)
        serializer_with_facility_1 = BusListSerializer(bus_with_facility_1)
        serializer_with_facility_2 = BusListSerializer(bus_with_facility_2)

        self.assertNotIn(serializer_without_facilities.data, response.data)
        self.assertIn(serializer_with_facility_1.data, response.data)
        self.assertIn(serializer_with_facility_2.data, response.data)

    def test_bus_retrieve(self) -> None:
        facility_1 = Facility.objects.create(name="test_1")
        facility_2 = Facility.objects.create(name="test_2")

        bus_with_facilities = sample_bus()
        bus_with_facilities.facilities.add(facility_1, facility_2)
        serializer = BusRetrieveSerializer(bus_with_facilities)

        url = detail_url(bus_with_facilities.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_bus_forbidden(self) -> None:
        payload = {
            "info": "AA 0000 AA",
            "num_seats": 40
        }
        response = self.client.post(BUS_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
