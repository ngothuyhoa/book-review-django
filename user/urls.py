from django.urls import path
from .views import ProfileUserView, FollowUserView
from . import views

app_name = 'user'
urlpatterns = [
    path('profile/<int:pk>', ProfileUserView.as_view(), name='profile-user'),
    path('follow/<int:pk>', FollowUserView.as_view(), name='follow-user'),
]
