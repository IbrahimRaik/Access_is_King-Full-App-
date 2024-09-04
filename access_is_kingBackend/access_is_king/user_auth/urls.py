from django.urls import path
from user_auth.views import (
    PasswordResetView, 
    UserLoginView, 
    UserRegistrationView, 
    GenerateBIDNumberView,  # Import the BID number generator view
)

urlpatterns = [
    path('signup', UserRegistrationView.as_view(), name='signup'),
    path('login', UserLoginView.as_view(), name='signin'),
    path('reset-password', PasswordResetView.as_view(), name='reset-password'),
    
    # BID Number Generator API
    path('generate-bid', GenerateBIDNumberView.as_view(), name='generate-bid'),
]
