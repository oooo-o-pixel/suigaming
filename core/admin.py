from django.contrib import admin
from .models import EventSlide


# Register your models here.
admin.site.site_header = "SuiGaming Admin"
admin.site.site_title = "SuiGaming Admin Portal"
admin.site.index_title = "Welcome to SuiGaming Admin Portal"


admin.site.register(EventSlide)
