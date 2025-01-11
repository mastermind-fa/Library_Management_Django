from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from core.views import Homeview

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin URL
    path('accounts/', include('accounts.urls')),  # Accounts app
    path('', Homeview.as_view(), name='home'),  # Home page
    path('transactions/', include('transactions.urls')),  # Transactions app
    path('books/', include('books.urls')),  # Books app
]


urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)