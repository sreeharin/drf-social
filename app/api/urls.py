from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from api.views import ProfileViewSet


router = DefaultRouter()
router.register('profile', ProfileViewSet, basename='profile')

app_name = 'api'
urlpatterns = router.urls
# urlpatterns=[
#     path('api/authenticate/', views.obtain_auth_token),
#     path('api/', include(router.urls)),
# ]