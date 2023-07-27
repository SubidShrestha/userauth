from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator,MinLengthValidator
from .manager import CustomUserManager

class CustomUser(AbstractUser):
    def image_upload(instance):
        return f'user/{instance.username}/{instance.photo}'
    
    phone_regex = RegexValidator(regex=r'(\+977)?[9]\d{9}$', message="Phone number must be entered in the format: '+9779876543210 or 9876543210' and must be 10 digits except for country code.")
    username = models.CharField(_("username"),max_length=26,unique=True)
    email = models.EmailField(_("email address"), unique=True)
    phone = models.CharField(validators=[phone_regex,MinLengthValidator(10)], max_length=14, unique=True)
    photo = models.ImageField(null=True,upload_to=image_upload)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ['username','email']

    objects = CustomUserManager()

    def __str__(self):
        return self.username