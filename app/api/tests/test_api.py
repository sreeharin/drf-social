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
from django.test import TestCase
from rest_framework.test import APIClient


class ProfileApiTests(TestCase):
    '''Tests for profile API'''
    def setUp(self) -> None:
        self.client = APIClient()

    def test_follow_profile(self):
        '''Test for following a profile'''

    def test_unfollow_profile(self):
        '''Test for unfollowing a profile'''

    def test_get_profile_detail(self):
        '''Test for getting details of a profile'''


class PostApiTests(TestCase):
    '''Test for post API'''
    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_post(self):
        '''Test for creating a post'''

    def test_delete_post(self):
        '''Test for deleting a post'''

    def test_delete_post_by_other_user(self):
        '''Test deleting another user's post raises an error'''

    def test_comment_post(self):
        '''Test for commenting on a post'''

    def test_like_post(self):
        '''Test for liking a post'''

    def test_dislike_post(self):
        '''Test for disliking a post'''

    def test_get_post_by_id(self):
        '''Test for view post details by id of post'''

    def test_all_posts_of_profile(self):
        '''Test for viewing all posts by a profile'''