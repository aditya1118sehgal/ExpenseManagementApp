from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# user profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=1, blank=False)

    def is_admin(self):
        return (self.role is 'A')

    def get_role(self):
        if self.is_admin():
            return 'Admin'
        else:
            return 'Regular'

    def __str__(self):
        return self.role


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
