from time import timezone
from rest_framework import serializers
from .models import Tournament, Registration

# Serializer for Tournament model
class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ['id', 'host', 'title', 'description', 'game_type', 'game_category',
                 'start_date', 'end_date', 'status', 'created_at', 'is_approved']
        
    def create(self, validated_data):
        host = validated_data['host']
        tournament = super().create(validated_data)

        # If host is a player, elevate them temporarily to host role
        if host.role == 'player':
            host.temporary_host_until = tournament.end_date
            host.save()

        return tournament
    
# Serializer for Registration model
class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = ['id', 'tournament', 'player', 'registered_at']

