from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Book
from django.shortcuts import render, redirect, get_object_or_404
from student_dash.models import BorrowRequest



@login_required
def home(request):
    return render(request, 'staff_dash/home.html')


@login_required
def add_staff(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        first_name = request.POST.get('first_name').strip()
        last_name = request.POST.get('last_name').strip()
        email = request.POST.get('email').strip()
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Basic validation
        if not all([username, first_name, last_name, email, password1, password2]):
            messages.error(request, "All fields are required.")
            return redirect('staff_dash:add_staff')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('staff_dash:add_staff')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('staff_dash:add_staff')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use.")
            return redirect('staff_dash:add_staff')

        # Create the staff user
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password1
        )
        user.is_staff = True
        user.save()

        messages.success(request, f"Staff member '{username}' added successfully.")
        return redirect('staff_dash:add_staff')

    return render(request, 'staff_dash/add_staff.html')


#adding a student
@login_required
def add_student(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        first_name = request.POST.get('first_name').strip()
        last_name = request.POST.get('last_name').strip()
        email = request.POST.get('email').strip()
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Basic validation
        if not all([username, first_name, last_name, email, password1, password2]):
            messages.error(request, "All fields are required.")
            return redirect('staff_dash:add_student')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('staff_dash:add_student')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('staff_dash:add_student')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use.")
            return redirect('staff_dash:add_student')

        # Create student user
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password1
        )
        user.is_staff = False
        user.save()
        messages.success(request, f"Student '{username}' added successfully.")
        return redirect('staff_dash:add_student')
    return render(request, 'staff_dash/add_student.html')



def upload_book(request):
    if request.method == "POST":
        title = request.POST.get('title')
        author = request.POST.get('author')
        genre = request.POST.get('genre')
        description = request.POST.get('description')
        publisher = request.POST.get('publisher')
        year = request.POST.get('year')
        cover_image = request.FILES.get('cover_image')
        file = request.FILES.get('file')

        # Physical or digital choice
        is_digital = request.POST.get('is_digital') == 'on'
        quantity_available = request.POST.get('quantity_available') or 0

        book = Book(
            title=title,
            author=author,
            genre=genre,
            description=description,
            publisher=publisher,
            year=year if year else None,
            cover_image=cover_image,
            file=file if is_digital else None,
            is_digital=is_digital,
            quantity_available=quantity_available
        )
        book.save()
        messages.success(request, f"Book '{title}' added successfully.")
        return redirect('staff_dash:upload_book')

    return render(request, 'staff_dash/upload_book.html')


@login_required
def analytics_dashboard(request):
    books = Book.objects.all()
    total_views = sum(b.views for b in books)
    total_downloads = sum(b.downloads for b in books)
    total_books = books.count()

    return render(request, 'staff_dash/analytics_dashboard.html', {
        'books': books,
        'total_views': total_views,
        'total_downloads': total_downloads,
        'total_books': total_books,
    })





@login_required
def manage_borrow_requests(request):
    requests_list = BorrowRequest.objects.select_related('student', 'book').order_by('-request_date')
    return render(request, 'staff_dash/manage_borrow_requests.html', {'requests': requests_list})


@login_required
def approve_request(request, pk):
    borrow_request = get_object_or_404(BorrowRequest, pk=pk)
    borrow_request.approve()
    messages.success(request, f"Approved borrow request for {borrow_request.student.username}")
    return redirect('staff_dash:manage_borrow_requests')


@login_required
def decline_request(request, pk):
    borrow_request = get_object_or_404(BorrowRequest, pk=pk)
    borrow_request.decline()
    messages.info(request, f"Declined borrow request for {borrow_request.student.username}")
    return redirect('staff_dash:manage_borrow_requests')
