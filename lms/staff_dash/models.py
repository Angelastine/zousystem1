from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    genre = models.CharField(max_length=100, blank=True)
    publisher = models.CharField(max_length=200, blank=True,null=True)
    year = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    # File uploads for digital books
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    pdf_file = models.FileField(upload_to='books/pdfs/', blank=True, null=True)
    docx_file = models.FileField(upload_to='books/docs/', blank=True, null=True)

    # ✅ Add this for digital books
    file = models.FileField(upload_to='books/', blank=True, null=True)

    # Hybrid library system
    is_digital = models.BooleanField(default=True)
    quantity_available = models.PositiveIntegerField(default=0)

    # Tracking
    views = models.PositiveIntegerField(default=0)
    downloads = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
