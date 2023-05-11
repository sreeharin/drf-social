import sys
from django.contrib.auth import get_user_model
from rest_framework import serializers
from core.models import (
    Profile,
    Post,
    Comment,
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
        return Post.objects.create(
            profile=self.context['request'].user.profile,
            post=validated_data['post'],
        )


class CommentSerializer(serializers.ModelSerializer):
    '''Comment serializer'''
    profile = ProfileSerializer(read_only=True)
    post = PostSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'profile', 'post', 'comment']

    def create(self, validated_data):
        post_id = self.context['request'].data.get('post_id', None)
        post = Post.objects.get(id=post_id)
        return Comment.objects.create(
            profile=self.context['request'].user.profile,
            post=post,
            comment=validated_data['comment']
        )


class ProfileDetailSerializer(serializers.ModelSerializer):
    '''Profile detail serializer'''
    user = UserSerializer(read_only=True)
    follows = FollowSerializer(many=True, read_only=True)
    following = FollowSerializer(many=True, read_only=True)
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'follows', 'following', 'posts']