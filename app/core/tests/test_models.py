'''
Tests which are done to the models include
1. Profile
    a. Get profile details
    b. Follow/Unfollow user

2. Post
    a. Upload post
    b. Delete post
    c. Like/Unlike post
    d. Comment on post
'''

from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Profile

def create_user(**kwargs):
    '''Helper function for creating new user'''
    user_details = {
        'username': 'test',
        'password': 'testpass123',
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'test@example.com',
        }
    user_details.update(kwargs)
    return get_user_model().objects.create(**user_details)


class ProfileModelTests(TestCase):
    '''Tests for profile model'''
    def test_create_profile(self) -> None:
        '''Test for creating a profile'''
        user = create_user()
        profiles = Profile.objects.count()
        self.assertEqual(profiles, 1)
        profile_exists = Profile.objects.filter(user=user).exists()
        self.assertTrue(profile_exists)

    def test_get_profile(self) -> None:
        '''Test for getting details of a profile'''
        user = create_user()
        profile = user.profile
        self.assertEqual(user.first_name, profile.user.first_name)
        self.assertEqual(user.last_name, profile.user.last_name)
        self.assertEqual(user.email, profile.user.email)

    def test_follow_profile(self) -> None:
        '''Test for following a profile'''
        user_1 = create_user()
        user_2 = create_user(username='test2')
        user_1.profile.follows.add(user_2.profile)
        self.assertIn(user_2.profile, user_1.profile.follows.all())

    def test_unfollow_profile(self) -> None:
        '''Test for unfollowing a profile'''
        user_1 = create_user()
        user_2 = create_user(username='test2')
        user_1.profile.follows.add(user_2.profile)
        self.assertIn(user_2.profile, user_1.profile.follows.all())
        user_1.profile.follows.remove(user_2.profile)
        self.assertNotIn(user_2.profile, user_1.profile.follows.all())


class PostModelTests(TestCase):
    '''Tests for post model'''
    def test_create_post(self) -> None:
        '''Test for creating a post'''

    def test_delete_post(self) -> None:
        '''Test for deleting a post'''

    def test_like_post(self) -> None:
        '''Test for liking a post'''

    def test_unlike_post(self) -> None:
        '''Test for unliking a post'''

    def test_like_unlike(self) -> None:
        '''Test for liking then unliking a post'''

    def test_unlike_like(self) -> None:
        '''Test for unliking the liking a post'''

    def test_comment_post(self) -> None:
        '''Test for commenting a post'''