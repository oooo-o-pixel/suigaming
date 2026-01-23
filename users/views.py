from django.shortcuts import render
from rest_framework import viewsets
from .models import User, Profile, Wallet
from .serializers import UserSerializer, ProfileSerializer, WalletSerializer
from .permissions import IsAdmin

# ViewSet for User model
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

# ViewSet for Profile model
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

# ViewSet for Wallet model
class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer