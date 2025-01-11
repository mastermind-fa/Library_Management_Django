from django.contrib import admin

# from transactions.models import Transaction
from .models import Transaction
from .views import send_mail


admin.site.register(Transaction)