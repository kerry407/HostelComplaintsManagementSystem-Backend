from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from .models import StudentUser, PorterUser

@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if not instance.is_porter:
            StudentUser.objects.create(user=instance)
        else:
            PorterUser.objects.create(user=instance)
    