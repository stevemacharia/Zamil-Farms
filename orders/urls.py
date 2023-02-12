from django.urls import path, include
from . import views
from django.conf import settings, urls
from django.conf.urls.static import static
urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('pdf_invoice/', views.LabelsView.as_view(), name='export-pdf'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
STATIC_URL = '/static/'