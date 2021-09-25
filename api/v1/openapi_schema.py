from rest_framework import status
from drf_yasg import openapi

reading_properties = {
    "reading": openapi.Schema(type=openapi.TYPE_NUMBER, description="Float"),
    "timestamp": openapi.Schema(
        type=openapi.TYPE_STRING, description="RFC3339 timestamp"
    ),
    "device_id": openapi.Schema(
        type=openapi.TYPE_STRING, description="valid UUID4 string"
    ),
    "customer_id": openapi.Schema(
        type=openapi.TYPE_STRING, description="valid UUID4 string"
    ),
}

add_event_schema_request = openapi.Schema(
    type=openapi.TYPE_ARRAY,
    items=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=reading_properties,
        required=["reading", "timestamp", "device_id", "customer_id"],
    ),
)
add_event_schema_response = {
    status.HTTP_201_CREATED: openapi.Schema(
        type=openapi.TYPE_ARRAY,
        items=openapi.Schema(type=openapi.TYPE_OBJECT, properties=reading_properties),
    ),
}
event_list_schema_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "device": openapi.Schema(
            type=openapi.TYPE_STRING, description="valid UUID4 string"
        ),
        "customer": openapi.Schema(
            type=openapi.TYPE_NUMBER, description="valid UUID4 string"
        ),
        "start_date": openapi.Schema(
            type=openapi.TYPE_NUMBER,
            description="Upper limit filter -> RFC3339 timestamp",
        ),
        "end_date": openapi.Schema(
            type=openapi.TYPE_NUMBER, description="Lower limit RFC3339 -> timestamp"
        ),
        "size": openapi.Schema(
            type=openapi.TYPE_NUMBER, description="Aggregation size, in minutes"
        ),
        "clean": openapi.Schema(
            type=openapi.TYPE_BOOLEAN,
            description="Remove Nan value, keep response clean",
        ),
    },
    required=["device", "customer"],
)
