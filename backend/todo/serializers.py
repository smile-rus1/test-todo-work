from rest_framework import serializers
from .models import Task, Category


class TaskBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'due_date']


class CategorySerializer(serializers.ModelSerializer):
    tasks = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'tasks']

    def get_tasks(self, obj):
        return TaskBriefSerializer(obj.tasks.all(), many=True).data


class TaskSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        queryset=Category.objects.all(),
        source='categories'
    )

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'user',
            'categories',
            'category_ids',
            'due_date',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
