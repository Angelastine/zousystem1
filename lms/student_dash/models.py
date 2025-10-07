from django.db import models
from django.contrib.auth.models import User
from staff_dash.models import Book
from django.utils import timezone
from datetime import timedelta

class BorrowRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
        ('returned', 'Returned'),
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    request_date = models.DateTimeField(default=timezone.now)
    return_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def approve(self):
        self.status = 'approved'
        self.return_date = timezone.now().date() + timedelta(days=14)
        self.book.quantity_available = max(0, self.book.quantity_available - 1)
        self.book.save()
        self.save()

    def decline(self):
        self.status = 'declined'
        self.save()

    def mark_returned(self):
        self.status = 'returned'
        self.book.quantity_available += 1
        self.book.save()
        self.save()

    def __str__(self):
        return f"{self.student.username} - {self.book.title} ({self.status})"
