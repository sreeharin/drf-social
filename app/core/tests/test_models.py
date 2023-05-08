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


class ProfileModelTests(TestCase):
    '''Tests for profile model'''
    def test_create_profile(self) -> None:
        '''Test for creating a profile'''

    def test_get_profile(self) -> None:
        '''Test for showing details of a profile'''

    def test_follow_profile(self) -> None:
        '''Test for following a profile'''

    def test_unfollow_profile(self) -> None:
        '''Test for unfollowing a profile'''


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