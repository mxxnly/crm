from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('Username is required')
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'    # Логін для входу
    REQUIRED_FIELDS = ['email']    # Поля обов’язкові при створенні

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    firstname = models.TextField(max_length=100, blank=True, null=True)
    lastname = models.TextField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    telegram_nickname = models.CharField(max_length=32, blank=True, null=True)
    profile_img = models.ImageField(upload_to="avatars/", blank=True, null=True)
    data_of_birth = models.DateField(blank=True, null=True)
    date_of_hire = models.DateField(blank=True, null=True)
    count_of_tasks = models.IntegerField(default=0)
    count_of_done_tasks = models.IntegerField(default=0)
    

    def __str__(self):
        return f"Profile of {self.user.username}"

