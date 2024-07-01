from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.contrib.auth.hashers import make_password


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        print('IN USERS')
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        print(user)
        user.set_password(password)
        print(user.password)
        # user.save(using=self._db)
        user.save()
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username, password, **extra_fields)

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']
    
    objects = CustomUserManager()

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_group_set',  # Custom related name to avoid clashes
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions '
                   'granted to each of their groups.'),
        related_query_name='custom_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_perms_set',  # Custom related name to avoid clashes
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='custom_user',
    )
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    class Meta:
        db_table = 'custom_user'
