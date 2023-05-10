from django.contrib.auth import get_user_model
from rest_framework import serializers
from core.models import Profile


class UserSerializer(serializers.ModelSerializer):
    '''User model serializer'''
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
        read_only_fields = ['id']


class FollowSerializer(serializers.ModelSerializer):
    '''Follower serializer'''
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['user']


class ProfileSerializer(serializers.ModelSerializer):
    '''Profile model serializer'''
    user = UserSerializer()
    follows = FollowSerializer(many=True)
    following = FollowSerializer(many=True)

    class Meta:
        model = Profile
        fields = ['user', 'follows', 'following']
