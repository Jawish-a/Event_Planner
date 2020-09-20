from django.urls import path
from .views import homepage, signin, signup, signout, dashboard, profile, not_found, event_create, event_list

urlpatterns = [
	path('', homepage, name='homepage'),
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('signout/', signout, name='signout'),
	path('dashboard', dashboard, name='dashboard'),
	path('profile/', profile, name='profile'),
	path('not-found/', not_found, name='not_found'),
    path('events/', event_list, name='event-list'),
    path('events/create/', event_create, name='event-create'),
]