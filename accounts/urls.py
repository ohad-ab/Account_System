from django.urls import  path
from accounts import views

urlpatterns = [
    path('', views.HomeView.as_view(), name = "home"),
    path('signup/', views.SignUpView.as_view(), name = 'signup'),
    path('profiles/<slug:slug>/', views.UserProfileView.as_view(), name = 'profile'),
    path('user-list/', views.UsersListView.as_view(), name="user-list"),
    path('friend_request/<slug:slug>/', views.SendFriendRequest.as_view(), name="friend-request"),
    path('friend_request_list', views.accept_friend_request.as_view(), name="accept-request"),
]