from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView, CreateAPIView
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User

from .serializers import RegisterSerializer, EventListSerializer, UserListSerializer
from events.models import Event, Follower
from datetime import datetime, timedelta


class Register(CreateAPIView):
	serializer_class = RegisterSerializer

class UpcommingEventsList(ListAPIView):
	queryset = Event.objects.filter(start_date__gte = datetime.now() )
	serializer_class = EventListSerializer
	filter_backends = [SearchFilter,OrderingFilter,]
	search_fields = ['name']
	permission_classes = [AllowAny]

class EventsList(ListAPIView):
	queryset = Event.objects.all()
	serializer_class = EventListSerializer
	filter_backends = [SearchFilter,OrderingFilter,]
	search_fields = ['name']
	permission_classes = [AllowAny]

class OrganizerEventsList(ListAPIView):
    serializer_class = EventListSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        organizer_obj = User.objects.get(id=self.kwargs['organizer_id'])
        return Event.objects.filter(organizer=organizer_obj)

# class MyEventsList(ListAPIView):
#     pass

# class MyFollowing(ListAPIView):
#     serializer_class = UserListSerializer
#     permission_classes = [IsAuthenticated]
#     def get_queryset(self):
#         print(self.request.user.following.all())
#         # user_followings = Follower.objects.filter(follower=self.request.user).follower
#         return self.request.user.following.follower.all()

