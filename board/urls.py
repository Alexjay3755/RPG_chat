from django.urls import path

from .views import Profile, ConfirmUser

urlpatterns = [
    path('', Profile.as_view(), name='profile' ),
    path('confirm_user/', ConfirmUser.as_view(), name='confirm_user' ),
]