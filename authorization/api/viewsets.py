from rest_framework import viewsets
from .serializers import CustomUserSerializer, PasswordResetRequestSerializer
from ..models import CustomUser, PasswordResetRequest
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.middleware.csrf import get_token
from rest_framework.permissions import AllowAny
from rest_framework import status
from datetime import datetime, timedelta
from django.utils import timezone
import socket
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
from django.http import HttpResponse, JsonResponse, QueryDict

class CustomUserViewset(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    
    def get_queryset(self):
        return CustomUser.objects.all()

class PasswordResetRequestViewSet(viewsets.ModelViewSet):
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        return PasswordResetRequest.objects.all()
    
    def create(self, request):
        email = request.data.get('email')
        
        if email:
            user = CustomUser.objects.get(email = request.data['email'])
        else    :
            return Response(
                {'error':'User not found.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        requests = PasswordResetRequest.objects.filter(user = user).order_by('-created')
        if len(requests) >0:
            now = timezone.now()
            threshold = now - timedelta(minutes=5)
            if (requests[0].created >= threshold and requests[0].is_active==True):
                return Response(
                    {
                        'error':'There is already an existing password reset request created within the last 5 mins. Please check your email.'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        for item in requests:
            item.is_active=False
            item.save()
        
        if isinstance(request.data, QueryDict):
            request.data._mutable = True
        request.data['user']=user.pk
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            request_obj = serializer.save()
            send_password_reset_email(request_obj)
            
            return Response(
                serializer.data,
                status=status.HTTP_200_OK            
            )
        return Response(
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['POST'])
@permission_classes([AllowAny])
def check_password_otp(request):
    code = request.data['otp']
    user = CustomUser.objects.get(email = request.data['email'])
    try:
        request_obj = PasswordResetRequest.objects.get(
        code=code,
        user = user
       )
        now = timezone.now()
        threshold = now - timedelta(minutes=5)
        if (now - request_obj.created <= timedelta(minutes=5) and request_obj.is_active==True):
            return Response(
            PasswordResetRequestSerializer(request_obj).data,
            status=status.HTTP_200_OK
            )
        return Response(
            {'error':'OTP timed out. Press resend to try again.'},
            status=status.HTTP_400_BAD_REQUEST
            
        )

    except PasswordResetRequest.DoesNotExist:
        return Response(
            {
                'error': 'Invalid OTP.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def get_csrf_token(request):
    csrf_token = get_token(request)
    return Response({'csrf_token': csrf_token})


def send_password_reset_email(resetRequest:PasswordResetRequest):
    
    html_message = render_to_string(
        'password_reset_email.html',
        {
            'resetRequest':resetRequest,
            'ip':get_server_ip()
        }
    )
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject = 'Password Reset',
        message = plain_message,
        from_email = settings.DEFAULT_FROM_EMAIL,
        recipient_list=[resetRequest.user.email],
        fail_silently=False,
        html_message=html_message
    )


def get_server_ip():
    try:
        # Get the hostname of the server
        hostname = socket.gethostname()
        # Get the IP address associated with the hostname
        server_ip = socket.gethostbyname(hostname)
        return server_ip
    except socket.error as err:
        # Handle the error if any
        return None