from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class SupportCase(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Support Case #{self.id}"

    class Meta:
        indexes = [models.Index(fields=["from_user"])]


class Message(models.Model):
    support_case = models.ForeignKey(SupportCase, on_delete=models.RESTRICT)
    from_user = models.ForeignKey(User, on_delete=models.RESTRICT)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["support_case"])]
