# Generated by Django 4.2.1 on 2023-05-14 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0004_rename_id_task_task_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='subtask',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='삭제 여부'),
        ),
    ]
