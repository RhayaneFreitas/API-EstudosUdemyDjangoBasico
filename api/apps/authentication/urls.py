from api.apps.authentication.views import user

from django.urls import(
    path,
    include
)

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('hello-viewset', user.HelloviewSet, basename='hello-viewset') # 
router.register('profile', user.UserProfileViewSet) # Não precisa especificar o basename.
router.register('feed', user.UserProfileFeedViewSet)

urlpatterns = [
    path(
        'hello-view/',
        user.HelloApiView.as_view()
    ),
    path(
        'login/',
        user.UserLoginApiView.as_view()
    ),
    path('',
        include(router.urls)
    )
]