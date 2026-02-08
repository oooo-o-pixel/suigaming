from django.db import models
from users.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def reset_temp_host(sender, instance, **kwargs):
    # Reset temporary host status if the date has passed
    if instance.end_date and instance.end_date < timezone.now():
        host = instance.host
        if host.role == 'player':
            host.temporary_host_until = None
            host.save()

# Tournament Model
class Tournament(models.Model):
    GAME_TYPES = [
        ('web2', 'Web2'),  # Traditional web2 game
        ('web3', 'Web3'),  # Blockchain based web3 game
    ]

    GAME_CATEGORIES = [
        ('fps', 'First Person Shooter'),  # FPS games
        ('action', 'Action'),  # Action games
        ('adventure', 'Adventure'),  # Adventure games
        ('strategy', 'Strategy'),  # Strategy games
        ('card', 'Card Games'),  # Card games
        #More categories can be added as needed
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),  # Tournament is awaiting approval
        ('upcoming', 'Upcoming'), # Tournament is scheduled but not started
        ('ongoing', 'Ongoing'),  # Tournament is currently happening
        ('completed', 'Completed'),  # Tournament has ended
        #More info can be added like cancelled, paused etc.
    ]

    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hosted_tournaments')  # Host of the tournament
    title = models.CharField(max_length=200)  # Title of the tournament
    subtitle = models.CharField(max_length=200, blank=True)  # Subtitle for the tournament, can be used in the swiper or tournament listing
    description = models.TextField()  # Description of the tournament
    game_type = models.CharField(max_length=10, choices=GAME_TYPES)  # Type of game
    game_category = models.CharField(max_length=20, choices=GAME_CATEGORIES, default='action')  # Category of the game
    start_date = models.DateTimeField()  # Start date and time
    end_date = models.DateTimeField()  # End date and time
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')  # Current status
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for tournament creation
    is_approved = models.BooleanField(default=False)  # Approval status by admin
    image = models.ImageField(upload_to="hero/", default="hero/image_1.jpg") # Image for the tournament, can be used in the swiper or tournament listing
    is_live = models.BooleanField(default=False) # Flag to indicate if the tournament is currently live, can be used to show live badge or highlight in the UI
    starting_soon = models.BooleanField(default=False)   # Flag to indicate if the tournament is starting soon, can be used to show starting soon badge or highlight in the UI
    start_time = models.DateTimeField(default=timezone.now) # This can be used to show countdown timers in the UI for upcoming tournaments
    button_text = models.CharField(max_length=50, default="View Tournament") # Customizable button text for the tournament card or swiper, can be used to create urgency like "Register Now" for upcoming tournaments or "Join Now" for live tournaments
    
    button_link = models.URLField( blank=True, null=True) # Customizable button link for the tournament card or swiper, can be used to direct users to the tournament details page, registration page or live stream link depending on the tournament status

    def __str__(self):
        return f"{self.title} ({self.game_type}-{self.game_category})"
    
# Registration Model
class Registration(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='registrations')  # Tournament being registered for
    player = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tournament_registrations')  # Player registering
    registered_at = models.DateTimeField(auto_now_add=True)  # Timestamp for registration

    class Meta:
        unique_together = ('tournament', 'player')  # Ensure a player can register only once per tournament

    def __str__(self):
        return f"{self.player.username} registered for {self.tournament.title}"