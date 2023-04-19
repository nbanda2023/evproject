from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
   

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'profile_picture']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    @property
    def is_admin(self):
        return self.is_staff

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    carmodel = models.CharField(max_length=200)
    license = models.CharField(max_length=20)
    plugtype = models.CharField(max_length=255)

    def __str__(self):
        return self.user.name







class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    connector_type = models.CharField(max_length=255)
    poi_name = models.CharField(max_length=255)
    poi_url = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.email} - {self.connector_type} - {self.poi_name}"

    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"


class Payment(models.Model):
    bookingId = models.CharField(max_length=255)
    cardNumber = models.CharField(max_length=16)
    cardHolder = models.CharField(max_length=255)
    expiryDate = models.CharField(max_length=5)
    cvc = models.CharField(max_length=3)
