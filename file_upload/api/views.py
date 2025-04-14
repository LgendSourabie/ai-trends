from file_upload.models import FileUpload
from rest_framework import generics
from file_upload.api.serializers import FileUploadSerializer


class fileView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = FileUpload.objects.all()
    serializer_class = FileUploadSerializer

        