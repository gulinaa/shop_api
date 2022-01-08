from django.contrib.auth.views import LogoutView
from django.urls import path

from account.views import RegistrationView, ActivationView, LoginView, ChangePasswordView, ForgotPassword

urlpatterns = [
    path('register/', RegistrationView.as_view()),
    path('activate/', ActivationView.as_view()),
    path('login/', LoginView.as_view()),
    # path('logout/', LogoutView.as_view()),
    path('change_password/', ChangePasswordView.as_view()),
    path('forgot_password/', ForgotPassword.as_view()),
]