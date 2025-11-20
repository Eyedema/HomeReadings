from django.urls import path
from .views import CSVUploadView, upload_page

urlpatterns = [
    path("", upload_page, name="upload-page"),
    path("upload-csv/", CSVUploadView.as_view(), name="upload-csv")
]