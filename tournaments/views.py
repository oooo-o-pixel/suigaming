from django.shortcuts import render
from rest_framework import viewsets
from .models import Tournament, Registration
from .serializers import TournamentSerializer, RegistrationSerializer
from users.permissions import IsAdmin, IsHostUser, IsPlayerUser, IsHostOrTempHost

# ViewSet for Tournament model
class TournamentViewSet(viewsets.ModelViewSet):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer

    # Only admins can approve tournaments, but hosts, players or admin can create and manage their own tournaments
    def get_permissions(self):
        if self.action in ['create']:
            return [IsHostOrTempHost()]
        elif self.action in ['approve', 'destroy', 'update', 'partial_update']:
            return [IsAdmin()]
        return [] # Allow read-only access for others i.e anyone can list or view tournaments

# ViewSet for Registration model
class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer

    # Only players can register for tournaments
    permission_classes = [IsPlayerUser]