# staff_dash/urls.py
from django.urls import path
from . import views

app_name = 'staff_dash'

urlpatterns = [
    path('', views.home, name='home'),
    path('add_staff/', views.add_staff, name='add_staff'),
    path('add_student/', views.add_student, name='add_student'),
    path('upload_book/', views.upload_book, name='upload_book'),
    path('analytics/', views.analytics_dashboard, name='analytics_dashboard'),
    path('manage-requests/', views.manage_borrow_requests, name='manage_borrow_requests'),
    path('approve/<int:pk>/', views.approve_request, name='approve_request'),
    path('decline/<int:pk>/', views.decline_request, name='decline_request'),
]
