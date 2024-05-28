from api.apps.authentication.models.user import ( # More specific than api.apps.authentication.models import user
    UserProfile,
    ProfileFeedItem
)

from rest_framework import serializers
from rest_framework.validators import UniqueValidator


from django.utils.translation import gettext_lazy as _
import datetime

class HelloSerializer(serializers.Serializer):
    """Serilizes a name field for testing our APIView"""
    name = serializers.CharField(max_length=10)
    
class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""
    
    class Meta:
        model = UserProfile
        fields = (
            'id',
            'email',
            'name',
            'password'
            
        )
        
        read_only_fields = ( # Just Read
            'id',
        )
        extra_kwargs = { # Avoid exposing passwords
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }       
        
    def create(self, validated_data): # Poderia ter utilizado o decorador transaction.atomic = Tratados com uma única transação, se falhar toda a operação reverte.
        """Create and Return a new User"""
        user = UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user
    
    def update(self, instance, validated_data):
        """Handle updating user account"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)    

class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """Serializes profile feed items"""

    class Meta:
        model = ProfileFeedItem
        fields = ('id',
                  'user_profile',
                  'status_text',
                  'created_on'
                  
        )
        extra_kwargs = {
            'user_profile': {
                'read_only': True}
        }    


'''class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(  # Oferece funcionalidades específicas para e-mail.
        required=True,
        validators=[
            UniqueValidator(
                queryset=UserProfile.objects.all(),
                message=_('This email is already in use.')
            )
        ]
    )'''