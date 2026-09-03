from django.urls import path
from . import views

urlpatterns = [
    path("test/", views.test_api, name="test_api"),
    path("upload/", views.upload_image, name="upload_image"),
    path("translate/", views.translate_text_api, name="translate_text_api"),
    path("languages/", views.get_languages, name="get_languages"),
]