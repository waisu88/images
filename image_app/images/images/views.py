from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import LoginSerializer


class LoginAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            username = data['username']
            password = data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return Response({"message": "You have been successfully logged in."})
            return Response(
                {"message": "error", "details": ["Invalid credentials"]})

login_api_view = LoginAPIView.as_view()


class LogoutAPIView(APIView):
    def get(self, request):
        logout(request)
        return Response({"message": "You have been logouted."})

logout_api_view = LogoutAPIView.as_view()
