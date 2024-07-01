from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from authorization.api.serializers import CustomUserSerializer

class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        email = data.get('email', '')
        password = data.get('password', '')
        print(email, password)
        user = authenticate(request=request, username=email, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            user_data = CustomUserSerializer(user).data
            return Response({
                'token': token.key,
                'user':user_data
            })
        else:
            return Response({'error': 'Authentication failed'}, status=status.HTTP_401_UNAUTHORIZED)
