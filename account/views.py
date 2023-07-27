from rest_framework.generics import CreateAPIView
from .models import CustomUser
from .serializers import UserRegistrationSerializer,LoginSerializer,LogoutSerializer
from rest_framework.response import Response
from rest_framework import status,permissions

class RegisterView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer

class LoginView(CreateAPIView):
    serializer_class = LoginSerializer

    def post(self, request,*args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
    
class LogoutView(CreateAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request,*args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response({'msg':'Logout Successful'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_401_UNAUTHORIZED)
