from django.urls import path
from . import views

app_name = 'profiles'
urlpatterns = [
    path('', views.ProfileListView.as_view(), name='all_profiles_list'),
    path('myprofile/', views.my_profile, name='my_profile_view'),
    path('<slug>', views.ProfileDetailView.as_view(), name='profile_detail_view'),
    path('my_invites/', views.invites_received_view, name='my_invites_view'),  
    # finish page to invite
    path('to_invite/', views.invite_profiles_list_view, name='invite_profiles_view'),
    path('send_invite/', views.send_invitation, name='send_invite'),
    path('remove_friend/', views.remove_from_friends, name='remove_friend'),
    path('my_invites/accept/', views.accept_invitation, name='accept_invite'),
    path('my_invites/reject/', views.reject_invitation, name='reject_invite'),
]