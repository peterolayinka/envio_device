from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from events.services import DeviceService
from events.serializers import ReadingSerializer

from .openapi_schema import (
    event_list_schema_request,
    add_event_schema_request,
    add_event_schema_response,
)


@swagger_auto_schema(
    method="post",
    request_body=event_list_schema_request,
)
@api_view(["POST"])
def event_list(request):
    """
    Retrieve a *Reading* by device_id or customer_id
    ---

    """
    device_service = DeviceService()
    result = device_service.get_reading(**request.data)

    if isinstance(result, dict) and result.get("error"):
        return Response(result, status=status.HTTP_400_BAD_REQUEST)

    return Response({"data": result}, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method="post",
    request_body=add_event_schema_request,
    responses=add_event_schema_response,
)
@api_view(["POST"])
def add_event(request):
    """
    Create new device reading
    ---

    """
    device_service = DeviceService()
    result = device_service.set_reading(request.data)
    if "error" in result:
        return Response(result, status=status.HTTP_400_BAD_REQUEST)

    serializer = ReadingSerializer(result, many=True)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
