from django.contrib import admin
from .models import Tournament, Registration

# Registering the Tournament model
@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ('title', 'host', 'game_type', 'game_category', 'status', 'start_date', 'end_date', 'created_at', 'is_approved')
    search_fields = ('title', 'host__username')
    list_filter = ('game_type', 'status', 'game_category')

# Registering the Registration model
@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('player', 'tournament', 'registered_at')
    search_fields = ('player__username', 'tournament__title')
    list_filter = ('tournament__game_type', 'tournament__status', 'tournament__is_approved')