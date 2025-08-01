from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.http import HttpResponseNotFound
from django.shortcuts import redirect

# Custom 404 redirect view
def custom_404_view(request, exception):
    return redirect('home')  # This redirects to the view named 'home'

urlpatterns = [
    path('', include('Model1.urls')),
    path('', include('Home.urls')),   # home view defined here
    path('', include('users.urls')),
    path('', include('Model2.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# Enable admin only in development
if settings.DEBUG:
    urlpatterns += [path('admin/', admin.site.urls)]
else:
    def block_admin(request):
        return HttpResponseNotFound("Page not found.")
    urlpatterns += [path('admin/', block_admin)]

# ✅ IMPORTANT: Must be at module level and AFTER urlpatterns
handler404 = custom_404_view
