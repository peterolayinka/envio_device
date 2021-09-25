import uuid

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from events.models import Customer, Device, Reading
from events.services import DeviceService


class DeviceAPITests(APITestCase):
    def setUp(self):
        self.customer_1 = uuid.uuid4()
        self.customer_2 = uuid.uuid4()
        self.customer_3 = uuid.uuid4()
        self.customer_4 = uuid.uuid4()
        self.device_1 = uuid.uuid4()
        self.device_2 = uuid.uuid4()
        self.device_3 = uuid.uuid4()
        self.device_4 = uuid.uuid4()
        self.device_5 = uuid.uuid4()
        self.device_6 = uuid.uuid4()
        self.device_7 = uuid.uuid4()
        self.device_8 = uuid.uuid4()
        self.add_reading_payload = [
            {
                "timestamp": "2021-09-23T00:07:28.261965+00:00",
                "reading": "1.1",
                "device_id": self.device_1,
                "customer_id": self.customer_1,
            },
            {
                "timestamp": "2021-09-23T00:07:28.261965+00:00",
                "reading": "1.2",
                "device_id": self.device_2,
                "customer_id": self.customer_2,
            },
            {
                "timestamp": "2021-09-23T00:07:28.261965+00:00",
                "reading": "1.3",
                "device_id": self.device_3,
                "customer_id": self.customer_3,
            },
            {
                "timestamp": "2021-09-23T00:07:28.261965+00:00",
                "reading": "1.4",
                "device_id": self.device_4,
                "customer_id": self.customer_4,
            },
            {
                "timestamp": "2021-09-21T00:07:28.261965+00:00",
                "reading": "1.5",
                "device_id": self.device_5,
                "customer_id": self.customer_1,
            },
            {
                "timestamp": "2021-09-22T00:07:28.261965+00:00",
                "reading": "1.6",
                "device_id": self.device_6,
                "customer_id": self.customer_1,
            },
            {
                "timestamp": "2021-09-24T00:07:28.261965+00:00",
                "reading": "1.7",
                "device_id": self.device_7,
                "customer_id": self.customer_2,
            },
            {
                "timestamp": "2021-09-20T00:07:28.261965+00:00",
                "reading": "1.8",
                "device_id": self.device_8,
                "customer_id": self.customer_3,
            },
            {
                "timestamp": "2021-09-20T00:07:28.261965+00:00",
                "reading": "1.9",
                "device_id": self.device_1,
                "customer_id": self.customer_1,
            },
            {
                "timestamp": "2021-09-20T00:08:28.261965+00:00",
                "reading": "2.9",
                "device_id": self.device_1,
                "customer_id": self.customer_1,
            },
        ]

    def test_event_list_without_error(self):
        device_service = DeviceService()
        device_service.set_reading(self.add_reading_payload)

        get_reading_payload = {"device": self.device_1}
        expected_device_value = 1
        current_value = 10
        url = reverse("event_list")
        self.assertEqual(Reading.objects.count(), current_value)
        response = self.client.post(url, get_reading_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["data"]), expected_device_value)

    def test_event_list_without_error_and_exclude_none_values(self):
        device_service = DeviceService()
        device_service.set_reading(self.add_reading_payload)

        get_reading_payload = {"device": self.device_1, "clean": True}
        expected_reading_value = 2
        expected_device_value = 1
        current_value = 10
        url = reverse("event_list")
        self.assertEqual(Reading.objects.count(), current_value)
        response = self.client.post(url, get_reading_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["data"]), expected_device_value)
        self.assertEqual(
            len(response.json()["data"][0]["readings"]), expected_reading_value
        )

    def test_event_list_without_error_and_exclude_none_values_for_contact_filter(self):
        device_service = DeviceService()
        device_service.set_reading(self.add_reading_payload)

        get_reading_payload = {"customer": self.customer_1}
        expected_device_value = 3
        current_value = 10
        url = reverse("event_list")
        self.assertEqual(Reading.objects.count(), current_value)
        response = self.client.post(url, get_reading_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["data"]), expected_device_value)

    def test_event_list_with_error_response(self):
        get_reading_payload = {}
        expected_value = {"error": "Please specify a device or customer id"}
        current_value = 0
        url = reverse("event_list")
        self.assertEqual(Reading.objects.count(), current_value)
        response = self.client.post(url, get_reading_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Reading.objects.count(), current_value)
        self.assertEqual(response.json(), expected_value)

    def test_add_event_without_error(self):
        expected_value = 10
        current_value = 0
        url = reverse("add_event")
        self.assertEqual(Reading.objects.count(), current_value)
        response = self.client.post(url, self.add_reading_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reading.objects.count(), expected_value)
        self.assertEqual(len(response.json()), expected_value)

    def test_add_event_with_error_response(self):
        get_reading_payload = {}
        expected_value = {"error": "Ensure you pass data as a list"}
        current_value = 0
        url = reverse("add_event")
        self.assertEqual(Reading.objects.count(), current_value)
        response = self.client.post(url, get_reading_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), expected_value)
