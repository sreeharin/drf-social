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
    follows = models.ManyToManyField('self', symmetrical=False, blank=True)


@receiver(models.signals.post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(instance, created, **kwargs) -> None:
    '''Create a profile when a new user is registered'''
    if created:
        profile = Profile(user=instance)
        profile.save()