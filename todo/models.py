from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    posted_at = models.DateTimeField(default=timezone.now)
    due_at = models.DateTimeField(null=True, blank=True)
    likes_count = models.PositiveIntegerField(default=0)  # いいね数を追加
    image = models.ImageField(upload_to='task_images/', null=True, blank=True)

    def is_overdue(self, dt):
        if self.due_at is None:
            return False
        return self.due_at < dt

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username}のコメント'

    def like(self):
        self.likes_count += 1
        self.save()
