from rest_framework import serializers

class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()
    target_language = serializers.CharField(required=False, default="en")

class TextTranslateSerializer(serializers.Serializer):
    text = serializers.CharField(required=True)
    source_language = serializers.CharField(required=False, default="auto")
    target_language = serializers.CharField(required=False, default="en")