import sys
from django.contrib.auth import get_user_model
from rest_framework import serializers
from core.models import (
    Profile,
    Post,
)


class UserSerializer(serializers.ModelSerializer):
    '''User model serializer'''
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
        read_only_fields = ['id']


class FollowSerializer(serializers.ModelSerializer):
    '''Follower serializer'''
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['user']


class ProfileSerializer(serializers.ModelSerializer):
    '''Profile model serializer'''
    user = UserSerializer(read_only=True)
    follows = FollowSerializer(many=True, read_only=True)
    following = FollowSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'follows', 'following']


class PostSerializer(serializers.ModelSerializer):
    '''Post model serializer'''
    profile = ProfileSerializer(read_only=True)
    likes = ProfileSerializer(many=True, read_only=True)
    dislikes = ProfileSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'profile', 'post', 'likes', 'dislikes']

    def create(self, validated_data):
        post = Post.objects.create(
            profile = self.context['request'].user.profile,
            post = validated_data['post'],
        )
        return post


class ProfileDetailSerializer(serializers.ModelSerializer):
    '''Profile detail serializer'''
    user = UserSerializer(read_only=True)
    follows = FollowSerializer(many=True, read_only=True)
    following = FollowSerializer(many=True, read_only=True)
    posts = PostSerializer(many=True, read_only= True)

    class Meta:
        model = Profile
        fields = ['user', 'follows', 'following', 'posts']