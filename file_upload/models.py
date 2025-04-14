from django.db import models

class FileUpload(models.Model):
    file = models.FileField(upload_to='', blank=True, null=True) 
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
