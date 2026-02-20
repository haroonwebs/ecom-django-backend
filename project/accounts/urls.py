from django.urls import path
from .views import RegisterUserView, UserLoginView, UserProfileView, UpdateUserPasswordView, SendResetPasswordEmailView, ResetPasswordView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/update-password/', UpdateUserPasswordView.as_view(), name='update-password'),
    path('send-reset-password-email/', SendResetPasswordEmailView.as_view(), name='email-reset-password'),
    path('reset-user-password/<uid>/<token>', ResetPasswordView.as_view(), name='reset-passward'),

]