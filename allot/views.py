from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
import os
import pandas as pd
from django.core.files.storage import default_storage
from .optimization import run_optimization

# Temporary storage for uploaded file path
TEMP_FILE_PATH = None  

class UploadFileView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        global TEMP_FILE_PATH
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "No file uploaded"}, status=400)

        # Save temporarily
        TEMP_FILE_PATH = default_storage.save(f"temp/{file.name}", file)

        # Read and preview the first few rows
        df = pd.read_excel(TEMP_FILE_PATH)
        preview_data = df.head(10).to_dict(orient="records")  # Convert to JSON

        return Response({"preview": preview_data})


class OptimizeView(APIView):
    def post(self, request, *args, **kwargs):
        global TEMP_FILE_PATH
        if not TEMP_FILE_PATH:
            return Response({"error": "No file uploaded"}, status=400)

        # Run optimization
        result = run_optimization(TEMP_FILE_PATH)

        # Delete temp file after processing
        os.remove(TEMP_FILE_PATH)
        TEMP_FILE_PATH = None  

        return Response(result)
