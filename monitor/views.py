from django.shortcuts import render
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

from .serializers import TemperatureReadingSerializer
from .models import TemperatureReading
from .helpers import rename_import_columns

import io
import csv

# Create your views here.

def upload_page(request):
    return render(request, "monitor/upload_page.html")

class CSVUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        upload = request.FILES.get("file")
        if not upload:
            return Response({"reason": "no file provided"}, status=status.HTTP_400_BAD_REQUEST)
    
        try:
            decoded = upload.read().decode("utf-8")
        except UnicodeDecodeError:
            return Response({"reason": "could not decode file as UTF-8"}, status=status.HTTP_400_BAD_REQUEST)
    
        io_string = io.StringIO(decoded)
        reader = csv.DictReader(io_string)

        BATCH_SIZE = 1000

        errors = []
        created = 0
        buffer = []

        with transaction.atomic():
            for index, row in enumerate(reader, start=2):
                row = rename_import_columns(row)
                serializer = TemperatureReadingSerializer(data=row)

                if not serializer.is_valid():
                    errors.append({"row": index, "errors": serializer.errors})
                    continue

                validated = serializer.validated_data
                buffer.append(TemperatureReading(**validated))

                if len(buffer) >= BATCH_SIZE:
                    TemperatureReading.objects.bulk_create(
                        buffer,
                        batch_size=BATCH_SIZE,
                        ignore_conflicts=True,
                    )
                    created += len(buffer)
                    buffer.clear()

            if buffer:
                TemperatureReading.objects.bulk_create(
                    buffer,
                    batch_size=BATCH_SIZE,
                    ignore_conflicts=True,
                )
                created += len(buffer)

        return Response(
            {"created": created, "errors": errors},
            status=status.HTTP_201_CREATED if created else status.HTTP_400_BAD_REQUEST,
        )