from django.urls import path

from .views import Profile, ConfirmUser, PostList, PostDetail, PostCreate

urlpatterns = [
    path('', Profile.as_view(), name='profile' ),
    path('confirm_user/', ConfirmUser.as_view(), name='confirm_user' ),
    path('posts/', PostList.as_view(), name='post_list' ),
    path('post/<int:pk>/', PostDetail.as_view(), name='post_detail' ),
    path('post/create/', PostCreate.as_view(), name='post_create' ),
]