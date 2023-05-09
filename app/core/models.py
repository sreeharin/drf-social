from django.db import models
from django.conf import settings
from django.dispatch import receiver


class Profile(models.Model):
    '''
    Profile model is an extension of `User` model provided by Django.
    It's automatically created when a new user is registered.
    '''
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='profile')
    follows = models.ManyToManyField(
        'self', symmetrical=False,
        blank=True, related_name='following')

    def __str__(self):
        return self.user.username


class Post(models.Model):
    '''Model for post'''
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='posts')
    post = models.CharField(max_length=512)
    likes = models.ManyToManyField(Profile, related_name='likes')
    dislikes = models.ManyToManyField(Profile, related_name='dislikes')


class Comment(models.Model):
    '''Model for comment'''
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    comment = models.CharField(max_length=128)


@receiver(models.signals.post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(instance, created, **kwargs) -> None:
    '''Create a profile when a new user is registered'''
    if created:
        profile = Profile(user=instance)
        profile.save()

@receiver(models.signals.m2m_changed, sender=Post.likes.through)
@receiver(models.signals.m2m_changed, sender=Post.dislikes.through)
def validate_like_dislike(sender, instance, action, pk_set, **kwargs) -> None:
    '''Function for validating likes and dislikes of a post'''
    if action == 'pre_add':
        '''pre_add: Sent before one or more objects are added to the relation.'''
        if sender == Post.dislikes.through and \
            instance.likes.filter(pk__in=pk_set).exists():
            '''Like is changed to dislike'''
            instance.likes.remove(*pk_set)
        elif sender == Post.likes.through and \
            instance.dislikes.filter(pk__in=pk_set).exists():
            '''Dislike is changed to like'''
            instance.dislikes.remove(*pk_set)