from django.db import models
from django.utils.timezone import now

from users.models import CustomUser as User

class Tweet(models.Model):
    '''
    related_name is used as an alias to populate all tweets created by a user
    '''
    user = models.ForeignKey(User, related_name='tweets', on_delete=models.CASCADE)
    content = models.TextField(max_length=280)
    created_at = models.DateTimeField(verbose_name='created at', default=now)
    updated_at = models.DateTimeField(verbose_name='updated at', null=True, default=None)

    class Meta:
        '''
        can also set ordering in view's queryset
        '''
        ordering = ['-created_at']