from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static   # ✅ required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('landing.urls')),          # landing app for login
    path('staff/', include('staff_dash.urls')), # staff dashboard
    path('student/', include('student_dash.urls')), # student dashboard
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)