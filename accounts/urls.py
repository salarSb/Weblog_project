from django.urls import path

from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('edit-profile/', views.EditProfileView.as_view(), name='edit-profile'),
]
