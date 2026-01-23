from django.db import models
from django.contrib.auth.models import AbstractUser #A class for customizing user models

#User Model
class User(AbstractUser): 
    ROLE_CHOICES = [
        ('admin', 'Admin'), #Admin access
        ('host', 'Host'), #Host access
        ('player', 'Player'), #Player access
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='player') #Role field with choices with player as default signed up user role
    temporary_host_until = models.DateTimeField(blank=True, null=True) #Field to store temporary host status until expiration date
    created_at = models.DateTimeField(auto_now_add=True) #Timestamp for user creation
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.username
    
#Profile Model
class Profile(models.Model):
    #One-to-one relationship with User model i.e each user has one profile and the profile is deleted if the user is deleted
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    display_name = models.CharField(max_length=100) #Display name
    created_at = models.DateTimeField(auto_now_add=True) #Timestamp for profile creation
    wallet_address = models.CharField(max_length=255, blank=True, null=True) #Wallet address field
    #Can add more fields like bio, avatar,etc.

    def __str__(self):
        return f"{self.display_name}'s Profile"
    
# Wallet Model
class Wallet(models.Model):
    WALLET_TYPES = [
        ("web2", "Web2"), #Traditional web2 wallet
        ("web3", "Web3"), #Blockchain based web3 wallet
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wallets') #Foreign key relationship with User model
    wallet_type = models.CharField(max_length=10, choices=WALLET_TYPES) #Type of wallet either web2 or web3
    wallet_address = models.CharField(max_length=255, unique=True) #Unique wallet address
    linked_at = models.DateTimeField(auto_now_add=True) #Timestamp for when the wallet was linked

    def __str__(self):
        return f"{self.user.username} - {self.wallet_type} Wallet"
    