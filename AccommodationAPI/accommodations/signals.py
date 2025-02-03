from django.db.models.signals import post_save
from django.dispatch import receiver
from accommodations.models import AcquistionArticle, FollowUser

@receiver(post_save, sender=AcquistionArticle)
def send_acquistion_notification(sender, instance, created, **kwargs):
    if created:
        followers = FollowUser.objects.filter(followed_user=instance.user)
        for follower in followers:
            print(follower)
            # send_push_notification(follower.user, f"{instance.user.username} has posted a new article: {instance.title}")