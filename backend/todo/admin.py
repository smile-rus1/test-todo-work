from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Category, Task, User


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'due_date', 'created_at', 'updated_at')
    list_filter = ('due_date', 'user', 'categories')
    search_fields = ('title', 'description')
    filter_horizontal = ('categories',)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'telegram_id', 'is_staff')
    search_fields = ('username', 'email')
