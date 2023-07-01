from django.contrib import admin
from .models import MenuItem, Order, TransactionTable, Table

admin.site.register([MenuItem, Order, TransactionTable, Table])