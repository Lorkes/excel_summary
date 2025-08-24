from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.parser.file_utils import process_file
from excel_summary.serializers import SummarySerializer


class SummaryViewSet(ViewSet):
    serializer_class = SummarySerializer
    parser_classes = [FormParser, MultiPartParser]

    def create(self, request: Request):
        """
        Upload a file with list of columns to summarize them

        Example payload:
        File: <file_to_upload>
        Columns: price;quantity

        Required fields:
        - `File`: Excel spreadsheet file to analyze
        - `Columns`: list of semicolon-separated (;) columns to summarize
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            file: InMemoryUploadedFile = request.data["file"]
            # stripping column names to avoid failure because
            # of spaces around ; for example
            columns: list[str] = [col.strip() for col in request.data["columns"].split(";")]
            result = process_file(file, columns)
            return Response(result, status=200)
        else:
            return Response(serializer.errors, status=400)
