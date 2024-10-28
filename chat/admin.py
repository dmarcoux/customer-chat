from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from chat.models import Message, SupportCase, User

admin.site.register(User, UserAdmin)
admin.site.register(SupportCase)
admin.site.register(Message)
