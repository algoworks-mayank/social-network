from django.urls import path
from .views import SignUpView, LoginView, UserSearchView, FriendRequestView, FriendListView, PendingFriendRequestsView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('search/', UserSearchView.as_view(), name='user-search'),
    path('friend-request/', FriendRequestView.as_view(), name='friend-request'),
    path('friend-request/<int:pk>/', FriendRequestView.as_view(), name='friend-request-action'),
    path('friends/', FriendListView.as_view(), name='friends-list'),
    path('pending-requests/', PendingFriendRequestsView.as_view(), name='pending-requests'),
]
