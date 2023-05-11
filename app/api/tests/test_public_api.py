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
from api.serializers import (
    ProfileDetailSerializer,
    PostSerializer,
)


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
        user = create_user(username='test_1')
        url = reverse('api:profile-follow', args=[user.profile.id])
        res = self.client.post(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        user.refresh_from_db()
        self.assertEqual(user.profile.follows.count(), 0)

    def test_unfollow_profile(self) -> None:
        '''Test for unfollowing profile by an anonymous user'''
        user = create_user(username='test_1')
        url = reverse('api:profile-unfollow', args=[user.profile.id])
        res = self.client.post(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_post(self) -> None:
        '''Test for creating post by an anonymous user'''
        url = reverse('api:post-list')
        payload = {
            'post': 'Sample Post',
        }
        res = self.client.post(url, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.count(), 0)

    def test_delete_post(self) -> None:
        '''Test delete post by an anonymous user'''
        user = create_user(username='test_1')
        post = create_post(profile=user.profile)
        url = reverse('api:post-detail', args=[post.id])
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.count(), 1)

    def test_like_post(self) -> None:
        '''Test for liking a post by an anonymous user'''
        user = create_user(username='test_1')
        post = create_post(profile=user.profile)
        url = reverse('api:post-like', args=[post.id])
        res = self.client.post(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        post.refresh_from_db()
        self.assertEqual(post.likes.count(), 0)

    def test_dislike_post(self) -> None:
        '''Test for unliking a post by an anonymous user'''
        user = create_user(username='test_1')
        post = create_post(profile=user.profile)
        url = reverse('api:post-dislike', args=[post.id])
        res = self.client.post(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        post.refresh_from_db()
        self.assertEqual(post.dislikes.count(), 0)

    def test_comment_post(self) -> None:
        '''Test for creating a comment by an anonymous user'''
        user = create_user(username='test_1')
        post = create_post(profile=user.profile)
        url = reverse('api:comment-list')
        payload = {
            'comment': 'Sample Comment',
            'post_id': post.id,
        }
        res = self.client.post(url, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        post.refresh_from_db()
        self.assertEqual(post.comments.count(), 0)

    def test_get_post_by_id(self) -> None:
        '''Test for viewing post by id'''
        user = create_user(username='test_1')
        post = create_post(profile=user.profile)
        url = reverse('api:post-detail', args=[post.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        post_serializer = PostSerializer(res.data)
        self.assertEqual(res.data, post_serializer.data)

    def test_get_posts_of_profile(self) -> None:
        '''Test for viewing all posts of a profile by an anonymous user'''
        user = create_user(username='test_1')
        create_post(profile=user.profile)
        create_post(profile=user.profile)
        url = reverse('api:post-list')
        res = self.client.get(url, {'profile': user.profile.id})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        posts_serializer = PostSerializer(res.data, many=True)
        self.assertEqual(len(posts_serializer.data), 2)