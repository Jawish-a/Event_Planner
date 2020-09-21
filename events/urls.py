from django.urls import path
from .views import (
    homepage, signin, signup, signout, dashboard,
    profile, profile_edit, user_edit, not_found,
    event_create, event_list, event_detail, event_edit,
    event_book, organizer, follow, unfollow
    )

urlpatterns = [
	path('', homepage, name='homepage'),
	path('not-found/', not_found, name='not_found'),
	path('dashboard', dashboard, name='dashboard'),

    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('signout/', signout, name='signout'),

	path('profile/', profile, name='profile'),
	path('organizer/<int:organizer_id>/', organizer, name='organizer'),
	path('profile/edit/', profile_edit, name='profile-edit'),
	path('user/edit/', user_edit, name='user-edit'),
    
    path('events/', event_list, name='event-list'),
    path('events/create/', event_create, name='event-create'),
    path('events/<int:event_id>/', event_detail, name='event-detail'),
    path('events/<int:event_id>/edit', event_edit, name='event-edit'),

    path('events/<int:event_id>/book/', event_book, name='event-book'),

    path('organizer/<int:organizer_id>/follow', follow, name='follow'),
    path('organizer/<int:organizer_id>/unfollow', unfollow, name='unfollow'),


]