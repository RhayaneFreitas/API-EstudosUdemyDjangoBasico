from django.db import models

from django.conf import settings
from django.contrib.auth.models import(
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager
)
from django.utils.translation import gettext_lazy as _


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""
    
    def create_user(self, email, name, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError("User must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name) # **
        user.set_password(password) # converts email to lowercase and removes unnecessary whitespace
        user.save(using=self._db) # Save user instance to database
        
        return user
    
    def create_superuser(self, email, name, password):
        """Create and save a new superuser with given details"""
        user = self.create_user(email, name, password)
        
        user.is_superuser = True # You didn't need to specify it because you were using PermissionMixin
        user.is_staff = True
        user.save(using=self.db)

        return user

class UserProfile(AbstractBaseUser,
           PermissionsMixin):
    
    email = models.EmailField(
        _('Email Address'),
        unique=True,
        max_length=255   
    )
    name = models.CharField(
        _('Name'),
        max_length=255   
    )
    is_active = models.BooleanField(
        _('Active'),
        default=True
    )
    is_staff = models.BooleanField(
        _('Staff'),
        default=False
    )

    objects = UserProfileManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    def get_full_name(self):
        """Retrieve full name of user"""
        return self.name
    
    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name
    
    def __str__(self):
        """Return string representation of our user"""
        return self.email

class ProfileFeedItem(models.Model):
    """Profile status update"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE # Está dizendo o que fazer quando o field remoto for deletado
    )
    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True) # Automatically add the date time stamp that the item was

    def __str__(self):
        """Return the model as a string"""
        return self.status_text