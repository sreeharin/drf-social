'''
Tests for API include
1. Profile
    a. Follow/Unfollow profile
    b. Get profile details
2. Post
    a. Create/Delete post
    b. Like/Dislike post
    c. Comment on post
    d. View post by id
    e. Return all posts of a user
'''
import sys
from typing import Type
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from rest_framework.test import APIClient
from rest_framework import status
from api.serializers import (
    ProfileSerializer,
    ProfileDetailSerializer,
    PostSerializer,
)
from core.models import Post, Profile


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


class ProfileApiTests(TestCase):
    '''Tests for profile API'''
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_follow_profile(self) -> None:
        '''Test for following a profile'''
        dummy_user = create_user(username='dummy')
        url = reverse('api:profile-follow', args=[dummy_user.id])
        res = self.client.post(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(dummy_user.profile, self.user.profile.follows.all())
        self.assertIn(self.user.profile, dummy_user.profile.following.all())
        user_serializer = ProfileSerializer(self.user.profile)
        dummy_serializer = ProfileSerializer(dummy_user.profile)
        self.assertEqual(
            user_serializer.data['follows'][0]['user'],
            dummy_serializer.data['user'])

    def test_follow_invalid_profile(self) -> None:
        '''Testing trying to follow invalid profile raises a 404 error'''
        url = reverse('api:profile-follow', args=[9])
        res = self.client.post(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_unfollow_profile(self) -> None:
        '''Test for unfollowing a profile'''
        dummy_user = create_user(username='dummy')
        # Follow
        url = reverse('api:profile-follow', args=[dummy_user.id])
        res = self.client.post(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(dummy_user.profile, self.user.profile.follows.all())
        self.assertIn(self.user.profile, dummy_user.profile.following.all())

        # Unfollow
        url = reverse('api:profile-unfollow', args=[dummy_user.id])
        res = self.client.post(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotIn(dummy_user.profile, self.user.profile.follows.all())
        self.assertNotIn(self.user.profile, dummy_user.profile.following.all())

    def test_unfollow_not_followed_profile(self) -> None:
        '''Test for unfollowing a profile which isn't followed'''
        dummy_user = create_user(username='dummy')
        url = reverse('api:profile-unfollow', args=[dummy_user.id])
        res = self.client.post(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_profile_detail(self) -> None:
        '''Test for getting details of a profile'''
        dummy_user = create_user(username='dummy')
        self.user.profile.follows.add(dummy_user.profile)
        url = reverse('api:profile-detail', args=[dummy_user.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        serializer = ProfileDetailSerializer(res.data)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(
            serializer.data['user']['first_name'], dummy_user.first_name)
        self.assertEqual(
            serializer.data['user']['last_name'], dummy_user.last_name)
        user_serializer = ProfileSerializer(self.user.profile)
        self.assertEqual(
            user_serializer.data['user'],
            serializer.data['following'][0]['user'])


class PostApiTests(TestCase):
    '''Test for post API'''
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_create_post(self) -> None:
        '''Test for creating a post'''
        url = reverse('api:post-list')
        payload = {
            'post': 'Sample post',
        }
        res = self.client.post(url, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        post_exists = Post.objects.filter(profile=self.user.profile).exists()
        self.assertTrue(post_exists)
        res_serializer = PostSerializer(res.data)
        post = Post.objects.filter(profile=self.user.profile)[0]

        self.assertEqual(
            res_serializer.data['profile']['user']['username'],
            self.user.username)
        self.assertEqual(res_serializer.data['post'], payload['post'])
        self.assertEqual(res_serializer.data['post'], post.post)
        self.assertEqual(res_serializer.data['id'], post.id)

    def test_delete_post(self) -> None:
        '''Test for deleting a post'''
        post = create_post(profile=self.user.profile)
        url = reverse('api:post-detail', args=[post.id])
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        post_exists = Post.objects.filter(id=post.id).exists()
        self.assertFalse(post_exists)

    def test_delete_post_by_other_user(self) -> None:
        '''Test deleting another user's post raises an error'''
        user = create_user(username='test_1')
        post = create_post(profile=user.profile)
        url = reverse('api:post-detail', args=[post.id])
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        post_exists = Post.objects.filter(id=post.id).exists()
        self.assertTrue(post_exists)


    def test_comment_post(self) -> None:
        '''Test for commenting on a post'''
        test_user = create_user(username='test_1')
        post = create_post(profile=test_user.profile)
        url = reverse('api:comment-list')
        payload = {
            'comment': 'Sample Comment',
            'post_id': post.id,
        }
        res = self.client.post(url, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        comment_exists = post.comments.filter(
            comment=payload['comment']).exists()
        self.assertTrue(comment_exists)
        comment = post.comments.all()[0]
        self.assertEqual(comment.comment, payload['comment'])
        self.assertEqual(comment.post.id, payload['post_id'])
        self.assertEqual(comment.profile, self.user.profile)

#     def test_like_post(self) -> None:
#         '''Test for liking a post'''

#     def test_dislike_post(self) -> None:
#         '''Test for disliking a post'''

#     def test_get_post_by_id(self) -> None:
#         '''Test for view post details by id of post'''

#     def test_all_posts_of_profile(self) -> None:
#         '''Test for viewing all posts by a profile'''


# class PublicApiTests(TestCase):
#     '''Test cases for anonymous user'''

#     def test_view_profile(self) -> None:
#         '''Test viewing profile by anonymous user'''

#     def test_follow_profile(self) -> None:
#         '''Test for following profile by anonymous user'''

#     def test_unfollow_profile(self) -> None:
#         '''Test for unfollowing profile by anonymous user'''