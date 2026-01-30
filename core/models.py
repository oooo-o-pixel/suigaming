from django.db import models
from django.utils import timezone

# Create your models here.

# note this is triumpstar doing I put dis on main cos i want u seing it 
# this is for the swipper page

# models.py
class EventSlide(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to="hero/")
    is_live = models.BooleanField(default=False)
    starting_soon = models.BooleanField(default=False)   
    start_time = models.DateTimeField()
    button_text = models.CharField(max_length=50, default="View Tournament")

    button_link = models.URLField( blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
