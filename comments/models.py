from django.db import models
from django.utils.timezone import now

from users.models import CustomUser as User
from tweets.models import Tweet

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField(max_length=280)
    created_at = models.DateTimeField(verbose_name='created at', default=now)
    updated_at = models.DateTimeField(verbose_name='updated at', null=True, default=None)

    class Meta:
        ordering = ['-created_at']