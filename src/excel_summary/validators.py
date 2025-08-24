from django.core.files import File
from rest_framework import serializers


def xlsx_file(filename: File) -> None:
    if not filename.name or not filename.name.endswith(".xlsx"):
        raise serializers.ValidationError(
            "Only '*.xlsx' files are supported. Select another file or update file extension"
        )
