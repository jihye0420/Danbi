from rest_framework import serializers

from users.serializers import TeamSerializer, UserInfoSerializer
from task.models import Task, SubTask


class TaskListSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)

    # create_user = UserProfileSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ('task_id', 'create_user', 'team',
                  'title', 'content', 'is_complete',
                  'completed_date', 'created_at', 'modified_at',)


class TaskDetailSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)
    create_user = UserInfoSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ('task_id', 'create_user', 'team',
                  'title', 'content', 'is_complete',
                  'completed_date', 'created_at', 'modified_at',)

    @classmethod
    def setup_preloading(cls, queryset):
        return queryset.select_related('team')


class TaskCreateSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)
    create_user = UserInfoSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ('team', 'task_id', 'title', 'content', 'create_user')


class TaskUpdateSerializer(serializers.ModelSerializer):
    team = TeamSerializer()
    create_user = UserInfoSerializer()

    class Meta:
        model = Task
        fields = ('team', 'title', 'content', 'create_user', 'is_complete')


class SubTaskDetailSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)

    class Meta:
        model = SubTask
        fields = ('subtask_id', 'team', 'is_complete',
                  'completed_date', 'created_at', 'modified_at')


class SubTaskCreateSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)

    class Meta:
        model = SubTask
        fields = ('team',)
