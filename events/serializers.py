from rest_framework import serializers

from .models import Reading, Device, Customer


class ReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reading
        fields = ["device", "customer", "timestamp", "reading"]
