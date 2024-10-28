from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class SupportCase(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["from_user"])]  # noqa: RUF012

    def __str__(self) -> str:
        return f"Support Case #{self.id}"


class Message(models.Model):
    support_case = models.ForeignKey(SupportCase, on_delete=models.RESTRICT)
    from_user = models.ForeignKey(User, on_delete=models.RESTRICT)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["support_case"])]  # noqa: RUF012

    def __str__(self) -> str:
        return f"Message #{self.id}"
