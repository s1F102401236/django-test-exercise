from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_remove_task_completed_remove_task_due_at_and_more'),
        ('todo', '0003_task_completed_task_due_at_alter_task_posted_at'),
    ]

    operations = [
        # 空のマージ用マイグレーション
    ]