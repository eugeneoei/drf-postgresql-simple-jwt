from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import CustomUser as User
from tweets.models import Tweet

class TweetReaction(models.Model):

    '''
    Using enums for reactions
    https://docs.djangoproject.com/en/3.2/ref/models/fields/#enumeration-types
    '''
    class Reactions(models.TextChoices):
        LIKE = 'LI', _('Like')
        DISLIKE = 'DI', _('Dislike')
        LOVE = 'LO', _('Love')
        SAD = 'SA', _('Sad')

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    reaction = models.CharField(max_length=2, choices=Reactions.choices)
