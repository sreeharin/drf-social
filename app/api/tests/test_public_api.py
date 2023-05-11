from typing import Type
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from rest_framework.test import APIClient
from rest_framework import status
from core.models import (
    Profile,
    Post,
)
from api.serializers import ProfileDetailSerializer


def create_user(**kwargs) -> Type[AbstractBaseUser]:
    '''Helper function for creating user'''
    user_details = {
        'username': 'test',
        'password': 'testpass123',
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'test@example.com',
    }
    user_details.update(kwargs)
    return get_user_model().objects.create(**user_details)

def create_post(profile: Profile=None) -> Post:
    '''Helper function for creating post'''
    if profile is None:
        user = create_user()
        profile = user.profile
    return Post.objects.create(
        profile=profile,
        post='Sample Post',
    )


class PublicApiTests(TestCase):
    '''Test cases for anonymous user'''
    def setUp(self) -> None:
        self.client = APIClient()

    def test_view_profile(self) -> None:
        '''Test viewing profile by an anonymous user'''
        user = create_user(username='test_1')
        url = reverse('api:profile-detail', args=[user.profile.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        profile_serializer = ProfileDetailSerializer(res.data)
        self.assertEqual(res.data, profile_serializer.data)

    def test_follow_profile(self) -> None:
        '''Test for following profile by an anonymous user'''

    def test_unfollow_profile(self) -> None:
        '''Test for unfollowing profile by an anonymous user'''

    def test_create_post(self) -> None:
        '''Test for creating post by an anonymous user'''

    def test_delete_post(self) -> None:
        '''Test delete post by an anonymous user'''

    def test_like_post(self) -> None:
        '''Test for liking a post by an anonymous user'''

    def test_unlike_post(self) -> None:
        '''Test for unliking a post by an anonymous user'''

    def test_create_comment(self) -> None:
        '''Test for creating a comment by an anonymous user'''

    def test_get_post_by_id(self) -> None:
        '''Test for viewing post by id'''

    def test_get_posts_of_profile(self) -> None:
        '''Test for viewing all posts of a profile by an anonymous user'''