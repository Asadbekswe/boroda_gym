import logging

from django.core.cache import cache
from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, ListAPIView, GenericAPIView
from rest_framework.response import Response

from apps.models import User
from apps.serializers import UserCreateSerializer, EmailModelSerializer, \
    VerifyModelSerializer
from apps.tasks import send_code_to_email
from apps.utils import sms_code

logger = logging.getLogger(__name__)


@extend_schema(tags=['Users'])
class UserCreateApiView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


@extend_schema(tags=['Users'])
class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class SendEmailAPIView(GenericAPIView):
    serializer_class = EmailModelSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        if cache.get(email):
            return Response(
                {"error": "Please wait before requesting a new code"},
                status=429
            )

        code = sms_code()
        cache.set(email, code, timeout=120)

        try:
            send_code_to_email.delay(email, code)
            logger.info(f"Verification code sent to {email}: {code}")
            return Response({"message": "Successfully sent code"})
        except Exception as e:
            cache.delete(email)
            logger.error(f"Failed to send email to {email}: {str(e)}")
            return Response(
                {"error": "Failed to send verification email"},
                status=500
            )

    def get_queryset(self):
        return self.request.user


class VerifyEmailAPIView(GenericAPIView):
    serializer_class = VerifyModelSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        code = serializer.validated_data['code']

        cached_code = cache.get(email)
        if cached_code != int(code):
            return Response({"error": "Invalid or expired code"}, status=400)

        cache.delete(email)
        return Response({"message": "Email verified successfully"})
