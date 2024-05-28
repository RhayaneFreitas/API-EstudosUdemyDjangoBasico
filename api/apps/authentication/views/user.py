from api.apps.authentication.models.user import (
    UserProfile
)
from rest_framework import (
    status,
    viewsets,
    filters,
)

from api.apps.authentication.serializers import user
from api.apps.authentication.serializers.user import HelloSerializer, UserProfileSerializer, ProfileFeedItemSerializer #######
from api.apps.authentication import permissions

from rest_framework.settings import api_settings
from rest_framework.authtoken.views import ObtainAuthToken ####
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ( ###
    ValidationError,
    NotFound
)
from rest_framework.permissions import(
    IsAuthenticated
)

from django.utils.translation import gettext_lazy as _

class HelloApiView(APIView):
# Added answer to our endpoints especificaly.
    """Test API View"""
    serializer_class = user.HelloSerializer
    
    def get(self,request,format=None):
        """Return a list of APIView features"""

        an_apiview = [
            'Uses HTTP methods as function (get, post, patch, put, delete)',
            'Is similar to a tradicional Django View',
            'Gives you the most control over you application logic',
            'Is mapped manually to URLS',
        ]

        return Response({'message': 'Hello!', 'an_apiview': an_apiview}) # Pode ser um dicionário ou lista.
    
    def post(self, request):
        """Create a hello message with our name"""
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response (
                {'messege': message}
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
                )
            
    def put(self, request, pk=None):
        """Handle updating object"""
        return Response({'method': 'PUT'})
    
    def patch(self, request, pk=None):
        """Handle parcial update of an object"""
        return Response({'method': 'PATCH'})

    def delete(self, request, pk=None):
        """Delete an object"""
        return Response({'method': 'DELETE'})
    
class HelloviewSet(viewsets.ViewSet):
    """Test API Viewset"""
    serializer_class = HelloSerializer ######
    
    def list(self, request):
        """Return a hello messsege"""

        a_viewset = [
            'Uses actions (list, create, retrieve, update, partial_update)',
            'Automatically maps to URLs using Routers',
            'Provides more functionality with less code',
        ]
        
        return Response({'messege': 'Hello!', 'a_viewset': a_viewset})
    
    def create(self, request):
        """Create a new hello message"""
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}!'
            return Response ({'message': message})
        else:

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
                )
            
    def retrieve(self, request, pk=None):
        """Handle getting an object by its ID"""
        return Response({'http_method': 'GET'})

    def update(self, request, pk=None):
        """Handle updating an object"""
        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        """Handle updating part of an object"""
        return Response({'http_method': 'PATCH'})
    
    def destroy(self, request, pk=None):
        """Handle removing an object"""
        return Response({'http_method': 'DELETE'})
    
class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = UserProfileSerializer
    queryset = user.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',) # Qual filtro que irá ser pesquisado.
    
class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES # Obtem o token
    
class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile feed items"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = ProfileFeedItemSerializer
    queryset = user.ProfileFeedItem.objects.all()
    permission_classes = (permissions.UpdateOwnStatus,IsAuthenticated)

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)