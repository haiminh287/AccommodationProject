from django.db.models.signals import post_save
from django.dispatch import receiver
from accommodations.models import AcquistionArticle, FollowUser
from accommodations.sendEmail import send_mail

@receiver(post_save, sender=AcquistionArticle)
def send_acquistion_notification(sender, instance, created, **kwargs):
    if created:
        followers = FollowUser.objects.filter(followed_user=instance.user)
        if followers:
            for follower in followers:
                email = follower.follower_user.email
                username = instance.user.username
                time = instance.created_at.strftime("%Y-%m-%d %H:%M:%S")
                titleArticle = instance.title
                price = instance.deposit
                phone = instance.user.phone
                location = instance.location
                
                send_mail(email, username, time, titleArticle, price, phone, location)