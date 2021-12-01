from django.urls import path

from .views import CommentCreateUpdateDestroy

app_name = 'comments'
urlpatterns = [
    path('', CommentCreateUpdateDestroy.as_view(), name='comments_create_update_destroy')
    # path('', CommentCreateUpdateDestroy.as_view({
    #     'post': 'create',
    #     'patch': 'partial_update',
    #     'delete': 'destroy'
    # }), name='comments_create_update_destroy')
]