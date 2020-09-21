from django.urls import path
from .views import homepage, signin, signup, signout, dashboard, profile, profile_edit, user_edit, not_found, event_create, event_list, event_detail, event_edit

urlpatterns = [
	path('', homepage, name='homepage'),
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('signout/', signout, name='signout'),
	path('dashboard', dashboard, name='dashboard'),
	path('profile/', profile, name='profile'),
	path('profile/edit', profile_edit, name='profile-edit'),
	path('user/edit', user_edit, name='user-edit'),
	path('not-found/', not_found, name='not_found'),
    path('events/', event_list, name='event-list'),
    path('events/create/', event_create, name='event-create'),
    path('events/<int:event_id>/', event_detail, name='event-detail'),
    path('events/<int:event_id>/edit', event_edit, name='event-edit'),
]