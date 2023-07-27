from rest_framework import serializers,exceptions
from .models import CustomUser
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = CustomUser
        fields=['email', 'username', 'photo', 'phone','password', 'password2']
        extra_kwargs={
            'password':{'write_only':True},
            'photo':{'required':False}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        return attrs

    def create(self, validate_data):
        validate_data.pop('password2')
        return CustomUser.objects.create_user(**validate_data)
    
class LoginSerializer(serializers.ModelSerializer):
    user = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    token = serializers.SerializerMethodField("get_tokens_for_user", read_only=True)

    def get_tokens_for_user(self,obj):
        user = CustomUser.objects.get(phone = obj.phone)
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    
    class Meta:
        model = CustomUser
        fields = ['user','password','token']

    def validate(self,attrs):
        username_field = attrs.get('user')
        password = attrs.get('password')
        try:
            user = CustomUser.objects.get(Q(username = username_field) | Q(phone=username_field))
            phone = user.phone
            LoginUser = authenticate(phone = phone,password = password)
            if LoginUser is not None:
                return LoginUser
            else:
                raise serializers.ValidationError('User with the credentials was not found.')
        except Exception as e:
            raise serializers.ValidationError('User with the credentials was not found.')
            
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):  # type: ignore
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):  # type: ignore
        try:
            RefreshToken(self.token).blacklist()
        except Exception as ex:
            print(ex)
            raise exceptions.AuthenticationFailed(ex)
        