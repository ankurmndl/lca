from django.urls import path
from .views import UploadFileView, OptimizeView

urlpatterns = [
    path("upload-file/", UploadFileView.as_view(), name="upload-file"),
    path("optimize/", OptimizeView.as_view(), name="optimize"),
]
