import pytz
import rfc3339
import pandas as pd
from dateutil.parser import parse
from itertools import groupby
from operator import itemgetter

from django.conf import settings

from .models import Device, Customer, Reading
from .forms import ReadingFormSetFactory, UUIDForm


def format_datetime(datetime):
    return rfc3339.rfc3339(datetime)


def convert_to_string(string):
    return str(string)


def find_customer_id(readings, device_id):
    reading = next(item for item in readings if item["device_id"] == device_id)
    return reading.get("customer_id")


class DeviceService:
    def set_device(self, id):
        device, _ = Device.objects.get_or_create(pk=id)
        return device

    def set_customer(self, id):
        customer, _ = Customer.objects.get_or_create(pk=id)
        return customer

    def set_reading(self, items):
        if not isinstance(items, list):
            return {"error": "Ensure you pass data as a list"}

        form_data = {
            "form-TOTAL_FORMS": len(items),
            "form-INITIAL_FORMS": 0,
        }
        for index, item in enumerate(items):
            form_data.update(
                {
                    f"form-{index}-reading": item.get("reading"),
                    f"form-{index}-timestamp": item.get("timestamp"),
                    f"form-{index}-device_id": item.get("device_id"),
                    f"form-{index}-customer_id": item.get("customer_id"),
                }
            )

        reading_form = ReadingFormSetFactory(form_data)
        if reading_form.is_valid():
            data = reading_form.save()
            return data
        else:
            return {"error": reading_form.errors}

    def filter_reading(
        self,
        device=None,
        customer=None,
        start_date=None,
        end_date=None,
        **kwargs,
    ):
        reading = Reading.objects

        if customer:
            uuid_form = UUIDForm({"id": customer})
            if uuid_form.is_valid():
                reading = reading.filter(customer__id=customer)
            else:
                return {"error": uuid_form.errors}

        if device:
            uuid_form = UUIDForm({"id": device})
            if uuid_form.is_valid():
                reading = reading.filter(device__id=device)
            else:
                return {"error": uuid_form.errors}

        if not customer and not device:
            return {"error": "Please specify a device or customer id"}

        if start_date:
            start_date = parse(start_date)
            if not settings.USE_TZ:
                start_date = pytz.utc.localize(start_date)
            reading = reading.filter(timestamp__gte=start_date)

        if end_date:
            end_date = parse(end_date)
            if not settings.USE_TZ:
                end_date = pytz.utc.localize(end_date)
            reading = reading.filter(timestamp__lte=end_date)

        return reading

    def get_reading(
        self,
        device=None,
        customer=None,
        start_date=None,
        end_date=None,
        size=5,
        clean=None,
        **kwargs,
    ):
        readings = self.filter_reading(device, customer, start_date, end_date)
        if isinstance(readings, dict) and readings.get("error"):
            return readings

        if not readings.exists():
            return []

        readings_df = pd.DataFrame(list(readings.values()))
        grouped_readings = (
            readings_df.groupby(["device_id"])
            .resample(f"{size or 5}T", on="timestamp")
            .agg({"reading": "mean", "customer_id": "first"})
        )

        if clean:
            grouped_readings = grouped_readings.dropna()
        else:
            grouped_readings = grouped_readings.fillna(0.0)

        reset_readings = grouped_readings.reset_index()

        reading_tuple = tuple(
            zip(
                reset_readings["device_id"],
                reset_readings["customer_id"],
                reset_readings["reading"],
                reset_readings["timestamp"],
            )
        )

        readings_dict = [
            {
                "device_id": convert_to_string(x[0]),
                "customer_id": convert_to_string(x[1]),
                "reading": x[2],
                "timestamp": format_datetime(x[3]),
            }
            for x in reading_tuple
        ]

        new_readings = [
            {
                "device_id": key,
                "customer_id": find_customer_id(readings_dict, key),
                "readings": [
                    {"timestamp": x["timestamp"], "reading": x["reading"]}
                    for x in value
                ],
            }
            for key, value in groupby(readings_dict, key=itemgetter("device_id"))
        ]

        return new_readings
