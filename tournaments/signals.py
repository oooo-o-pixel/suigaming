from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Tournament

@receiver(post_save, sender=Tournament)
def update_tournament_status(sender, instance, **kwargs):
    now = timezone.now()
    new_status = instance.status

    if instance.is_approved:
        if instance.start_date > now:
            new_status = 'upcoming'
        elif instance.start_date <= now < instance.end_date:
            new_status = 'ongoing'
        elif instance.end_date < now:
            new_status = 'completed'

    if new_status != instance.status:
        Tournament.objects.filter(pk=instance.pk).update(status=new_status)
