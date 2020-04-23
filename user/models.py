from django.db import models

from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, *args, **kwargs):
        if not email:
            raise ValueError("User must have an email address!")

        user = self.model(email=self.normalize_email(email), *args, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, *args, **kwargs):
        user = self.create_user(email, password, *args, **kwargs)
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create_publisher(self, email, password=None, *args, **kwargs):
        user = self.create_user(email, password, *args, **kwargs)
        user.is_publisher = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=False)
    is_publisher = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'

    @property
    def me(self):
        return self.profile

    def __str__(self):
        return self.email


class UserInfo(models.Model):
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    bio = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='profiles/', blank=True, null=True)

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile',
        blank=True, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
