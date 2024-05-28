from django.contrib import admin

from api.apps.authentication.models import user

admin.site.register(user.UserProfile)
admin.site.register(user.ProfileFeedItem)
### Lapidar