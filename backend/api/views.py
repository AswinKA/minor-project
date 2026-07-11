from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ImageUploadSerializer
from django.core.files.storage import default_storage
from ocr.extract import extract_text

@api_view(["GET"])
def test_api(request):
    return Response({
        "message": "AI Signboard Reader API is working!"
    })

@api_view(["POST"])
def upload_image(request):
    serializer = ImageUploadSerializer(data=request.data)

    if serializer.is_valid():
        image = serializer.validated_data["image"]

        file_path = default_storage.save(image.name, image)
        image_path = default_storage.path(file_path)

        text = extract_text(image_path)

        return Response({
            "text": text
        })

    return Response(serializer.errors, status=400)