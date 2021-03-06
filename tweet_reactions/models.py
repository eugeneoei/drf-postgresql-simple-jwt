from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import CustomUser as User
from tweets.models import Tweet

class Reactions(models.TextChoices):
    LIKE = 'LI', _('Like')
    DISLIKE = 'DI', _('Dislike')
    LOVE = 'LO', _('Love')
    SAD = 'SA', _('Sad')

class TweetReaction(models.Model):

    '''
    Using enums for reactions
    https://docs.djangoproject.com/en/3.2/ref/models/fields/#enumeration-types
    '''

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, related_name='reactions', on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=Reactions.choices)
