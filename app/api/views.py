import sys
from django.shortcuts import get_object_or_404
from rest_framework import (
    viewsets,
    status,
    mixins,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from core.models import (
    Profile,
    Post,
    Comment,
)
from api.serializers import (
    ProfileDetailSerializer,
    PostSerializer,
    CommentSerializer,
)


class ProfileViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    Profile viewset
    Provides views for viewing a profile, following/unfollowing a profile
    '''
    queryset = Profile.objects.all()
    serializer_class = ProfileDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['POST'])
    def follow(self, request, pk=None):
        '''Custom action for following a profile'''
        target_profile = self.get_object()
        user = request.user
        user.profile.follows.add(target_profile)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def unfollow(self, request, pk=None):
        '''Custom action for unfollowing a profile'''
        target_profile = self.get_object()
        user = request.user
        user.profile.follows.remove(target_profile)
        return Response(status=status.HTTP_200_OK)


class PostViewSet(
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        mixins.CreateModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet
    ):
    '''Post viewset'''
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        '''Filter queryset by profile id'''
        queryset = Post.objects.all()
        profile = self.request.query_params.get('profile')
        if profile is not None:
            queryset = queryset.filter(profile=profile)
        return queryset

    def destroy(self, request, pk=None):
        '''Only authorized person can delete a post'''
        target_post = self.get_object()
        profile = request.user.profile

        if target_post.profile != profile:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return super().destroy(request, pk=pk)

    @action(detail=True, methods=['POST'])
    def like(self, request, pk=None):
        '''Custom action for liking a post'''
        target_post = self.get_object()
        target_post.likes.add(request.user.profile)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def dislike(self, request, pk=None):
        '''Custom action for disliking a post'''
        target_post = self.get_object()
        target_post.dislikes.add(request.user.profile)
        return Response(status=status.HTTP_200_OK)


class CommentViewSet(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        viewsets.GenericViewSet
    ):
    '''Comment viewset'''
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]