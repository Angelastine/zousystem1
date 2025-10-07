from django.http import FileResponse
import os
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from staff_dash.models import Book
from .models import BorrowRequest
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    query = request.GET.get('q', '')
    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(genre__icontains=query)
        )
    else:
        books = Book.objects.all()

    context = {
        'books': books,
        'query': query,
    }
    return render(request, 'student_dash/home.html', context)






def books(request):
    query = request.GET.get('q', '')
    books = Book.objects.all()

    if query:
        books = books.filter(
            models.Q(title__icontains=query) |
            models.Q(author__icontains=query) |
            models.Q(genre__icontains=query)
        )

    context = {
        'books': books,
        'query': query,
    }
    return render(request, 'student_dash/books.html', context)


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    # Increment view count
    book.views += 1
    book.save(update_fields=['views'])
    return render(request, 'student_dash/book_detail.html', {'book': book})

def download_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.downloads += 1
    book.save()
    file_path = book.file.path
    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))


@login_required
def student_home(request):
    query = request.GET.get('q')
    books = Book.objects.all()
    if query:
        books = books.filter(title__icontains=query) | books.filter(author__icontains=query) | books.filter(genre__icontains=query)

    return render(request, 'student_dash/home.html', {'books': books, 'query': query})


@login_required
def borrow_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if not book.is_digital and book.quantity_available > 0:
        existing = BorrowRequest.objects.filter(student=request.user, book=book, status='pending').exists()
        if not existing:
            BorrowRequest.objects.create(student=request.user, book=book)
            messages.success(request, f"Borrow request for '{book.title}' submitted successfully.")
        else:
            messages.warning(request, "You already have a pending request for this book.")
    else:
        messages.error(request, "This book is not available for borrowing.")
    return redirect('student_dash:home')


