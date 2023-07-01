from django.contrib import admin

from .models import User, Profile, Branch, Customer

admin.site.register([User, Profile, Branch, Customer])

