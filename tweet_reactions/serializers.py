from rest_framework import serializers

from .models import TweetReaction, Reactions


class TweetReactionSerializer(serializers.ModelSerializer):

    type = serializers.ChoiceField(required=True, choices=Reactions)
    '''
    fields that are choices has a get_<field>_display method. refer to TweetReaction model
    '''
    type_display = serializers.CharField(
        source='get_type_display',
        read_only=True
    )
    user_id = serializers.PrimaryKeyRelatedField(
        source='user.id',
        read_only=True
    )

    class Meta:
        model = TweetReaction
        fields = (
            'id',
            'user_id',
            'type',
            'type_display'
        )

    def validate(self, data):
        '''
        validate that a user can only react once to a tweet
        '''
        request = self.context.get('request')
        print(request.method)
        tweet_id = self.context.get('view').kwargs.get('tweet_pk')
        if request.method == 'POST':
            try:
                tweet_reaction = TweetReaction.objects.get(
                    user=request.user,
                    tweet=tweet_id
                )
                raise serializers.ValidationError({
                    'error': f'Already reacted with {tweet_reaction.get_type_display()}. Cannot react more than once to a Tweet. Did you mean to update reaction?'
                })
            except TweetReaction.DoesNotExist:
                return data
        else:
            return data

