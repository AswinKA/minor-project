import time
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.files.storage import default_storage

from .serializers import ImageUploadSerializer, TextTranslateSerializer
from ocr.extract import extract_text
from ocr.language import detect_language
from ocr.translator import translate_text, LANG_MAP


SUPPORTED_LANGUAGES = [
    {"code": "en", "name": "English"},
    {"code": "ne", "name": "Nepali"},
    {"code": "hi", "name": "Hindi"},
    {"code": "es", "name": "Spanish"},
    {"code": "fr", "name": "French"},
    {"code": "de", "name": "German"},
    {"code": "ja", "name": "Japanese"},
    {"code": "zh-CN", "name": "Chinese (Simplified)"},
    {"code": "ar", "name": "Arabic"},
    {"code": "ko", "name": "Korean"},
]


@api_view(["GET"])
def test_api(request):
    return Response({
        "status": "online",
        "message": "AI Signboard Reader API is running successfully!",
        "ocr_engine": "Tesseract OCR (eng+nep)",
        "translation_engine": "Google Translate API"
    })


@api_view(["POST"])
def upload_image(request):
    serializer = ImageUploadSerializer(data=request.data)

    if serializer.is_valid():
        start_time = time.time()
        image = serializer.validated_data["image"]
        target_lang = serializer.validated_data.get("target_language", "en")

        file_path = default_storage.save(image.name, image)
        image_path = default_storage.path(file_path)

        # Perform OCR
        extracted_text = extract_text(image_path)

        # Detect language if text was found
        detected_lang = detect_language(extracted_text) if extracted_text else "en"

        # Translate text using Google Translator API
        translation = translate_text(
            extracted_text,
            source=detected_lang,
            target=target_lang
        )

        processing_time = round(time.time() - start_time, 2)

        return Response({
            "text": extracted_text,
            "detected_language": detected_lang,
            "translation": translation,
            "target_language": target_lang,
            "processing_time_seconds": processing_time,
            "image_url": f"/media/{file_path}"
        })

    return Response(serializer.errors, status=400)


@api_view(["POST"])
def translate_text_api(request):
    serializer = TextTranslateSerializer(data=request.data)

    if serializer.is_valid():
        text = serializer.validated_data["text"]
        source = serializer.validated_data.get("source_language", "auto")
        target = serializer.validated_data.get("target_language", "en")

        if source == "auto":
            detected_lang = detect_language(text)
        else:
            detected_lang = source

        translation = translate_text(text, source=detected_lang, target=target)

        return Response({
            "original_text": text,
            "source_language": detected_lang,
            "target_language": target,
            "translation": translation
        })

    return Response(serializer.errors, status=400)


@api_view(["GET"])
def get_languages(request):
    return Response({
        "languages": SUPPORTED_LANGUAGES
    })