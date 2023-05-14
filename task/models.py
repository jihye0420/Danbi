from django.db import models
from django.utils import timezone

from users.models import User, Team


class Task(models.Model):
    task_id = models.BigAutoField(primary_key=True)
    create_user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name='task_user',
                                    verbose_name='작성자')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=False, blank=False, related_name='task_team',
                             verbose_name='작성팀')
    title = models.CharField(max_length=255, null=False, blank=False, verbose_name='제목')
    content = models.TextField(null=True, blank=True, verbose_name='내용')
    is_complete = models.BooleanField(default=False, verbose_name='완료 여부')
    completed_date = models.DateTimeField(null=True, blank=True, verbose_name='완료일')
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False,
                                      verbose_name='생성 일자')
    modified_at = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name='수정 일자')

    class Meta:
        managed = True
        verbose_name_plural = "업무"
        db_table = 'Task'


class SubTask(models.Model):
    subtask_id = models.AutoField(primary_key=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=False, blank=False, related_name='subtask_user',
                             verbose_name='할당 팀')
    is_complete = models.BooleanField(default=False, verbose_name='완료 여부')
    completed_date = models.DateTimeField(null=True, blank=True, verbose_name='완료일')
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False,
                                      verbose_name='생성 일자')
    modified_at = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name='수정 일자')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=False, blank=False, related_name='subtask_task',
                             verbose_name='상위 업무')
    is_delete = models.BooleanField(default=False, verbose_name='삭제 여부')

    class Meta:
        managed = True
        verbose_name_plural = "하위 업무"
        db_table = 'SubTask'
