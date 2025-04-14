from rest_framework import serializers
from file_upload.models import FileUpload

class FileUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = FileUpload
        fields = "__all__"
        read_only_fields = ['uploaded_at','updated_at']