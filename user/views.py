import random

from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, exceptions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from twilio.rest import Client
from .models import CustomUser
from .serializers import RegistrationSerializer, RegistrationUpdateSerializer
from config import settings



def generate_verification_code():
    return str(random.randint(1000, 9999))


def send_verification_sms(phone_number, verification_code):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    message = client.messages.create(
        body=f'Your verification code is: {verification_code}',
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone_number
    )


class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = RegistrationSerializer
    http_method_names = ['post', 'get']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        registration = serializer.instance
        verification_code = generate_verification_code()
        registration.verification_code = verification_code
        registration.save()

        send_verification_sms(registration.phone_number, verification_code)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    def generate_verification_code(self):
        return str(random.randint(1000, 9999))


class PhoneVerifyView(APIView):
    def post(self, request):
        data = request.data

        user = CustomUser.objects.filter(verification_code=data['verification_code']).first()

        if user.is_verified:
            return Response({'message': 'You already verified your phone number'})

        if not user:
            raise exceptions.NotFound('User not found!')

        if data['verification_code'] != int(user.verification_code):
            raise exceptions.APIException('Code is incorrect!')
        user.is_verified = True
        user.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'You successfully verified your phone number',
            'status': 'success',
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })


class RegisterUpdateView(generics.GenericAPIView):
    serializer_class = RegistrationUpdateSerializer

    @swagger_auto_schema(request_body=RegistrationUpdateSerializer,
                         responses={200: 'User updated successfully', 400: 'Bad Request'})
    def put(self, request):
        user = request.user

        serializer = RegistrationUpdateSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User updated successfully'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):

    def post(self, request):

        data = request.data

        user = CustomUser.objects.filter(phone_number=data['phone_number']).first()
        verification_code = generate_verification_code()
        user.verification_code = verification_code

        user.save()

        send_verification_sms(user.phone_number, verification_code)

        return Response({"message": "We sent verification code"})


class LoginPhoneView(APIView):
    def post(self, request):
        data = request.data

        user = CustomUser.objects.filter(verification_code=data['verification_code']).first()

        if not user:
            raise exceptions.NotFound('User not found!')

        if data['verification_code'] != int(user.verification_code):
            raise exceptions.APIException('Code is incorrect!')

        user.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })
