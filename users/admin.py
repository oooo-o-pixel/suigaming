from django.contrib import admin
from .models import User, Profile, Wallet

# Registering the custom User model
admin.site.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'created_at')
    search_fields = ('username', 'email')

# Registering the Profile model
admin.site.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_name', 'created_at')
    search_fields = ('user__username', 'display_name')

# Registering the Wallet model
admin.site.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'wallet_type', 'wallet_address', 'linked_at')
    search_fields = ('user__username', 'wallet_address')