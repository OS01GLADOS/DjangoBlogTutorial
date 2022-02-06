from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from blog.models import Post


class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    date_posted = models.DateTimeField(default=timezone.now)
    content = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f'Comment {self.id} on post {self.post.title}'

    class Meta:
        ordering = ['date_posted']
