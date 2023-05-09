import sys
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from core.models import Profile
from api.serializers import ProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    @action(detail=True, methods=['POST'])
    def follow(self, request, pk=None):
        '''Custom action for following a profile'''
        target_profile = self.get_object()
        user = request.user
        user.profile.follows.add(target_profile)
        user.profile.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def unfollow(self, request, pk=None):
        '''Custom action for unfollowing a profile'''
        target_profile = self.get_object()
        user = request.user
        user.profile.follows.remove(target_profile)
        user.profile.save()
        return Response(status=status.HTTP_200_OK)

