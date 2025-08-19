from django.urls import path

from apps.views import UserCreateApiView, UserListAPIView, SendEmailAPIView, VerifyEmailAPIView, \
    ForgetPasswordGenericAPIView

urlpatterns = [

    path('users/', UserListAPIView.as_view()),
    path('user-create/', UserCreateApiView.as_view()),

    # Forgot password
    path('user-forgot-password/', ForgetPasswordGenericAPIView().as_view()),

    # Auth
    path('auth/send-email', SendEmailAPIView.as_view(), name='send_email'),
    path('auth/verify-code', VerifyEmailAPIView.as_view(), name='verify-email'),

]
