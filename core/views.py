from django.shortcuts import render
from tournaments.models import Tournament
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q

def events_view(request):
    now = timezone.now()
    two_days_later = now + timedelta(days=2)

    # Filter: live OR starting soon within 2 days
    slides = Tournament.objects.filter(
        Q(is_live=True) | Q(starting_soon=True, start_time__lte=two_days_later)
    )

    # Calculate countdowns for coming soon slides
    for slide in slides:
        if slide.starting_soon:
            delta = slide.start_time - now
            if delta.total_seconds() > 0:
                days = delta.days
                hours, remainder = divmod(delta.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                slide.countdown = f"{days} day{'s' if days!=1 else ''} " \
                                  f"{hours} hr{'s' if hours!=1 else ''} " \
                                  f"{minutes} min {seconds} sec"
            else:
                slide.countdown = "Starting soon!"
        else:
            slide.countdown = None  # live slides don't need countdown

    return render(request, "core/index.html", {"slides": slides})



def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')

