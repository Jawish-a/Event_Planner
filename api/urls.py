from django.urls import path
from api import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import EventsList, UpcommingEventsList, OrganizerEventsList #, MyFollowing

urlpatterns = [
    path('signin/', TokenObtainPairView.as_view(), name="api-signin"),
    path('signup/', views.Register.as_view(), name="api-signup"),
    path('events/', views.EventsList.as_view(), name="api-event-list"), 
    path('events/upcomming/', views.UpcommingEventsList.as_view(), name="api-upcomming-event-list"), 
    path('events/<organizer_id>/', views.OrganizerEventsList.as_view(), name="api-organizer-event-list"), 
    # path('my-events/', views.MyEventsList.as_view(), name="api-my-event-list"), 
    # path('my-following/', views.MyFollowing.as_view(), name="api-my-following-list"), 

]