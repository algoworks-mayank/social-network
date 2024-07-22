from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from .models import User, FriendRequest
from .serializers import UserSerializer, LoginSerializer, FriendRequestSerializer
from datetime import timedelta
from .pagination import UserPagination

class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh_token': str(refresh),
            'access_token': str(refresh.access_token),
        })

class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = UserPagination

    def get_queryset(self):
        query = self.request.query_params.get('q', '').lower()
        if '@' in query:
            return User.objects.filter(email__iexact=query)
        return User.objects.filter(username__icontains=query)

class FriendRequestView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):

        to_user_id = request.data.get('to_user_id')
        if not to_user_id:
            return Response({"error": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            to_user = User.objects.get(id=to_user_id)
            print("svvdsvsvszdvsdzv", to_user)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if user has sent more than 3 friend requests in the last minute
        one_minute_ago = timezone.now() - timedelta(minutes=1)
        recent_requests = FriendRequest.objects.filter(from_user=request.user, created_at__gte=one_minute_ago)
        if recent_requests.count() >= 3:
            return Response({"error": "You can only send 3 friend requests per minute."}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        FriendRequest.objects.create(from_user=request.user, to_user=to_user, status='pending')
        return Response({"message": "Friend request sent"}, status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        try:
            friend_request = FriendRequest.objects.get(id=pk, to_user=request.user)
        except FriendRequest.DoesNotExist:
            return Response({"error": "Friend request not found."}, status=status.HTTP_404_NOT_FOUND)
        
        action = request.data.get('action')
        if action == 'accept':
            friend_request.status = 'accepted'
            friend_request.save()
            return Response({"message": "Friend request accepted"}, status=status.HTTP_200_OK)
        elif action == 'reject':
            friend_request.status = 'rejected'
            friend_request.save()
            return Response({"message": "Friend request rejected"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)

class FriendListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return User.objects.filter(
            id__in=FriendRequest.objects.filter(from_user=self.request.user, status='accepted').values_list('to_user_id', flat=True)
        ) | User.objects.filter(
            id__in=FriendRequest.objects.filter(to_user=self.request.user, status='accepted').values_list('from_user_id', flat=True)
        )

class PendingFriendRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user, status='pending')