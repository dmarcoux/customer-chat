from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, SupportCase, Message

admin.site.register(User, UserAdmin)
admin.site.register(SupportCase)
admin.site.register(Message)
