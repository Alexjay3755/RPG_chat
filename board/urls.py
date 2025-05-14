from django.urls import path

from .views import Profile, ConfirmUser, PostList, PostDetail, PostCreate, comment_accept, comment_delete
urlpatterns = [
    path('', Profile.as_view(), name='profile' ),
    path('confirm_user/', ConfirmUser.as_view(), name='confirm_user' ),
    path('posts/', PostList.as_view(), name='post_list' ),
    path('post/<int:pk>/', PostDetail.as_view(), name='post_detail' ),
    path('post/create/', PostCreate.as_view(), name='post_create' ),
    path('comment/<int:pk>/accept/', comment_accept, name='comment_accept' ),
    path('comment/<int:pk>/delete/', comment_delete, name='comment_delete' ),
]