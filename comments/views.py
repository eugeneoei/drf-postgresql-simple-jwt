from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import APIException

from .models import Comment
from .serializers import CommentSerializer
from .permissions import IsCommentOwner
from tweets.models import Tweet


class CommentCreateUpdateDestroy(CreateModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        tweet = get_object_or_404(Tweet, pk=self.kwargs.get('pk'))
        serializer.save(user=self.request.user, tweet=tweet)

    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = (permissions.IsAuthenticated,)

        elif self.request.method in ['PATCH', 'DELETE']:
            permission_classes = (permissions.IsAuthenticated, IsCommentOwner)

        else:
            raise APIException('Nice Try!')

        return [permission() for permission in permission_classes]

