import string
import secrets

from django.contrib.auth.models import AbstractUser
from django.db import models


def generate_custom_id(length=12):
    """
    Генерация случайных pk для моделей.
    """
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


class User(AbstractUser):
    id = models.CharField(
        primary_key=True,
        max_length=12,
        default=generate_custom_id,
        editable=False
    )
    password = models.CharField(max_length=255, null=False)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    telegram_id = models.BigIntegerField(null=True)


class Category(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=12,
        default=generate_custom_id,
        editable=False
    )
    name = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='categories',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Category(id={self.id}, name={self.name})"


class Task(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=12,
        default=generate_custom_id,
        editable=False
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    categories = models.ManyToManyField(Category, related_name='tasks', blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Task(id={self.id}, title={self.title}, description={self.description}), categories={self.categories}"
