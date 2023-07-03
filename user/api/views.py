from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken
from .serializers import RegisterUserSerializer, LoginSerializer
from django.contrib.auth.hashers import make_password



# Registring a new user API
@api_view(['POST'])
@permission_classes([])
def registerUser(request):
    serializer = RegisterUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    # encrypt password
    serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
    
    user = serializer.save()
    _, token = AuthToken.objects.create(user)

    return Response({
        'message': 'You have signed up successfully !',
        'token'  : token
    })


# Login API
@api_view(['POST'])
@permission_classes([])
def login(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.validated_data
    _, token = AuthToken.objects.create(user)

    return Response({
        'message': 'logged in successfully !',
        'token'  : token
    })


# Get user info API
@api_view(['GET'])
@permission_classes([])
def getUser(request):
    user = request.user

    if user.is_authenticated:
        return Response({
            'first_name'  : user.first_name,
            'lastt_name'  : user.last_name,
            'username'    : user.username,
            'email'       : user.email,
            'password'    : user.password,
            'phone_number': user.phone_number,
            # 'avatar'      : user.avatar
        })

    return Response({'error': 'not authenticated'}, status=400)