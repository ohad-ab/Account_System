from django.urls import  path
from accounts import views

urlpatterns = [
    path('', views.HomeView.as_view(), name = "home"),
    path('signup/', views.SignUpView.as_view(), name = 'signup'),
    path('profiles/<slug:slug>/', views.UserProfileView.as_view(), name = 'profile'),
    path('user-list/', views.UsersListView.as_view(), name="user-list"),
]