from django.contrib.auth import authenticate
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication


from .serializers import UserSerializer
from .permissions import IsAuthenticatedOrCreateOnly


@api_view(['POST'])
def login_user(request):
    email = request.data.get('email', None)
    password = request.data.get('password', None)

    user = authenticate(email=email, password=password)
    if not user:
        response = {'message': 'Invalid credentials'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    serializer = UserSerializer(user)
    tokens = user.get_tokens()

    response = {'message': 'User logged in', 'user': serializer.data,
                'access_token': tokens['access'], 'refresh_token': tokens['refresh']}
    return Response(response, status=status.HTTP_200_OK)


class UserAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrCreateOnly]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

        # TODO: send out an email

        response = {'message': 'Done', 'user': serializer.data}
        return Response(response, status=status.HTTP_200_OK)

    def get(self, request):
        serializer = UserSerializer(request.user)

        response = serializer.data
        return Response(response, status=status.HTTP_200_OK)

    def put(self, request):
        request.user.update(request.data)

        serializer = UserSerializer(request.user)

        response = {'message': 'Done', 'user': serializer.data}
        return Response(response, status=status.HTTP_200_OK)

    def delete(self, request):
        request.user.delete()

        response = {'message': 'Done'}
        return Response(response, status=status.HTTP_200_OK)
