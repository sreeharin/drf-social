from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from api.views import (
    ProfileViewSet,
    PostViewSet,
)


router = DefaultRouter()
router.register('profile', ProfileViewSet, basename='profile')
router.register('post', PostViewSet, basename='post')

app_name = 'api'
urlpatterns = router.urls
# urlpatterns=[
#     path('api/authenticate/', views.obtain_auth_token),
#     path('api/', include(router.urls)),
# ]