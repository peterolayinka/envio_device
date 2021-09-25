import uuid

from django.test import TestCase

from events.models import Customer, Device, Reading
from events.services import DeviceService

# Create your tests here.


class ModelTestCase(TestCase):
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
        self.payload = [
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
        ]

    def test_set_device_when_device_id_doesnt_exist(self):
        expected_value = 1
        current_value = 0
        _uuid = uuid.uuid4()
        current_device = Device.objects.count()
        self.assertEqual(current_device, current_value)
        device_service = DeviceService()
        result = device_service.set_device(_uuid)
        expected_device = Device.objects.count()
        self.assertEqual(expected_device, expected_value)
        self.assertEqual(result.pk, _uuid)

    def test_set_device_when_device_already_exist(self):
        expected_value = 1
        current_value = 1
        _uuid = uuid.uuid4()
        device_service = DeviceService()
        result_1 = device_service.set_device(_uuid)
        current_device = Device.objects.count()
        self.assertEqual(current_device, current_value)
        self.assertEqual(result_1.pk, _uuid)
        result_2 = device_service.set_device(_uuid)
        expected_device = Device.objects.count()
        self.assertEqual(expected_device, expected_value)
        self.assertEqual(result_2.pk, _uuid)

    def test_set_customer_when_customer_id_doesnt_exist(self):
        expected_value = 1
        current_value = 0
        _uuid = uuid.uuid4()
        current_customer = Customer.objects.count()
        self.assertEqual(current_customer, current_value)
        device_service = DeviceService()
        result = device_service.set_customer(_uuid)
        expected_customer = Customer.objects.count()
        self.assertEqual(expected_customer, expected_value)
        self.assertEqual(result.pk, _uuid)

    def test_set_customer_when_customer_already_exist(self):
        expected_value = 1
        current_value = 1
        _uuid = uuid.uuid4()
        device_service = DeviceService()
        result_1 = device_service.set_customer(_uuid)
        current_customer = Customer.objects.count()
        self.assertEqual(current_customer, current_value)
        self.assertEqual(result_1.pk, _uuid)
        result_2 = device_service.set_customer(_uuid)
        expected_customer = Customer.objects.count()
        self.assertEqual(expected_customer, expected_value)
        self.assertEqual(result_2.pk, _uuid)

    def test_set_reading(self):
        expected_value = 9
        current_value = 0
        device_service = DeviceService()
        current_reading = Reading.objects.count()
        self.assertEqual(current_reading, current_value)
        result = device_service.set_reading(self.payload)
        current_reading = Reading.objects.count()
        self.assertEqual(current_reading, expected_value)
        self.assertEqual(len(result), expected_value)

    def test_set_reading_with_invalid_device(self):
        self.payload[2]["device_id"] = "invalid_device"
        expected_result = {"error": [{}, {}, {"device_id": ["Enter a valid UUID."]}, {}, {}, {}, {}, {}, {}]}
        current_value = 0
        device_service = DeviceService()
        current_reading = Reading.objects.count()
        self.assertEqual(current_reading, current_value)
        result = device_service.set_reading(self.payload)
        current_reading = Reading.objects.count()
        self.assertEqual(current_reading, current_value)
        self.assertEqual(result, expected_result)

    def test_set_reading_with_invalid_customer(self):
        self.payload[2]["customer_id"] = "invalid_customer"
        expected_result = {"error": [{}, {}, {"customer_id": ["Enter a valid UUID."]}, {}, {}, {}, {}, {}, {}]}
        current_value = 0
        device_service = DeviceService()
        current_reading = Reading.objects.count()
        self.assertEqual(current_reading, current_value)
        result = device_service.set_reading(self.payload)
        current_reading = Reading.objects.count()
        self.assertEqual(current_reading, current_value)
        self.assertEqual(result, expected_result)

    def test_set_reading_with_invalid_reading(self):
        self.payload[2]["reading"] = "invalid_reading"
        expected_result = {"error": [{}, {}, {"reading": ["Enter a number."]}, {}, {}, {}, {}, {}, {}]}
        current_value = 0
        device_service = DeviceService()
        current_reading = Reading.objects.count()
        self.assertEqual(current_reading, current_value)
        result = device_service.set_reading(self.payload)
        current_reading = Reading.objects.count()
        self.assertEqual(current_reading, current_value)
        self.assertEqual(result, expected_result)

    def test_set_reading_with_invalid_timestamp(self):
        self.payload[2]["timestamp"] = "invalid_timestamp"
        expected_result = {"error": [{}, {}, {"timestamp": ["Enter a valid date/time."]}, {}, {}, {}, {}, {}, {}]}
        current_value = 0
        device_service = DeviceService()
        current_reading = Reading.objects.count()
        self.assertEqual(current_reading, current_value)
        result = device_service.set_reading(self.payload)
        current_reading = Reading.objects.count()
        self.assertEqual(current_reading, current_value)
        self.assertEqual(result, expected_result)

    def test_ensure_device_can_only_be_assigned_to_one_customer(self):
        self.payload[1]["device_id"] = self.device_1
        self.payload[1]["customer_id"] = self.customer_2

        self.payload[3]["device_id"] = self.device_3
        self.payload[3]["customer_id"] = self.customer_2

        expected_result = {"error": [
            {},
            {
                "device_id": [
                    "Device ID can't be shared across customers, a device can only be assigned to one customer"
                ]
            },
            {},
            {
                "device_id": [
                    "Device ID can't be shared across customers, a device can only be assigned to one customer"
                ]
            },
            {}, {}, {}, {}, {},
        ]}
        current_value = 0
        device_service = DeviceService()
        current_reading = Reading.objects.count()
        self.assertEqual(current_reading, current_value)
        result = device_service.set_reading(self.payload)
        current_reading = Reading.objects.count()
        self.assertEqual(current_reading, current_value)
        self.assertEqual(result, expected_result)

    def test_get_reading_by_customer_id(self):
        current_value = 0
        expected_value = 9
        device_service = DeviceService()
        current_reading = Reading.objects.count()
        self.assertEqual(current_reading, current_value)
        set_result = device_service.set_reading(self.payload)
        current_reading = Reading.objects.count()
        self.assertEqual(current_reading, expected_value)
        self.assertEqual(len(set_result), expected_value)
        expected_value = 3
        get_result = device_service.get_reading(customer=self.customer_1, clean=True)
        self.assertEqual(len(get_result), expected_value)

    def test_get_reading_by_device_id(self):
        current_value = 0
        expected_value = 9
        device_service = DeviceService()
        current_reading = Reading.objects.count()
        self.assertEqual(current_reading, current_value)
        set_result = device_service.set_reading(self.payload)
        current_reading = Reading.objects.count()
        self.assertEqual(current_reading, expected_value)
        self.assertEqual(len(set_result), expected_value)
        expected_value = 2
        get_result = device_service.get_reading(device=self.device_1, clean=True)
        self.assertEqual(len(get_result[0]["readings"]), expected_value)

    def test_get_reading_by_customer_and_device_id(self):
        current_value = 0
        expected_value = 9
        device_service = DeviceService()
        current_reading = Reading.objects.count()
        self.assertEqual(current_reading, current_value)
        set_result = device_service.set_reading(self.payload)
        current_reading = Reading.objects.count()
        self.assertEqual(current_reading, expected_value)
        self.assertEqual(len(set_result), expected_value)
        expected_value = 1
        get_result = device_service.get_reading(
            device=self.device_2, customer=self.customer_2
        )
        self.assertEqual(len(get_result), expected_value)

    def test_get_reading_without_customer_or_device_id(self):
        current_value = 0
        expected_value = {"error": "Please specify a device or customer id"}
        device_service = DeviceService()
        current_reading = Reading.objects.count()
        self.assertEqual(current_reading, current_value)
        get_result = device_service.get_reading()
        current_reading = Reading.objects.count()
        self.assertEqual(current_reading, current_value)
        self.assertEqual(get_result, expected_value)

    def test_get_reading_filtered_by_start_time(self):
        current_value = 0
        expected_value = 9
        device_service = DeviceService()
        current_reading = Reading.objects.count()
        self.assertEqual(current_reading, current_value)
        set_result = device_service.set_reading(self.payload)
        current_reading = Reading.objects.count()
        self.assertEqual(current_reading, expected_value)
        self.assertEqual(len(set_result), expected_value)
        expected_value = 3
        get_result = device_service.get_reading(
            customer=self.customer_1, start_date="2021-09-21T00:00:00"
        )
        self.assertEqual(len(get_result), expected_value)

    def test_get_reading_filtered_by_end_time(self):
        current_value = 0
        expected_value = 9
        device_service = DeviceService()
        current_reading = Reading.objects.count()
        self.assertEqual(current_reading, current_value)
        set_result = device_service.set_reading(self.payload)
        current_reading = Reading.objects.count()
        self.assertEqual(current_reading, expected_value)
        self.assertEqual(len(set_result), expected_value)
        expected_value = 1
        get_result = device_service.get_reading(
            customer=self.customer_1, end_date="2021-09-21T00:00:00"
        )
        self.assertEqual(len(get_result), expected_value)
