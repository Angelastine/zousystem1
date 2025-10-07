# student_dash/urls.py
from django.urls import path
from . import views

app_name = 'student_dash'

urlpatterns = [
    path('', views.home, name='home'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('book/<int:pk>/download/', views.download_book, name='download_book'),
    path('borrow/<int:pk>/', views.borrow_book, name='borrow_book'),

]
