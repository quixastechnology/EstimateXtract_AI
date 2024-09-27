from django.db import models

# Create your models here.

class Estimate(models.Model):
    pdf_file = models.FileField(upload_to='uploads/')
    created_at = models.DateTimeField(auto_now_add=True)