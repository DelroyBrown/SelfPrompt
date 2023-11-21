from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import home, render_form, save_image

urlpatterns = [
    path('', render_form, name='render_form'),  # For handling GET requests to the homepage
    path('submit/', home, name='home'),  # For handling POST requests
     path('save_image/', save_image, name='save_image'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)