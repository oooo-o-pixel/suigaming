from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from users.models import User
from tournaments.models import Tournament

class TournamentLifecycleTests(TestCase):
    def setUp(self):
        self.host = User.objects.create_user(username="host", password="hostpass", role="host")

    def test_tournament_moves_to_upcoming_when_approved(self):
        tournament = Tournament.objects.create(
            host=self.host,
            title="Future Tournament",
            description="Starts later",
            game_type="web2",
            game_category="action",
            start_date=timezone.now() + timedelta(days=2),
            end_date=timezone.now() + timedelta(days=3),
            is_approved=True
        )
        tournament.refresh_from_db()
        self.assertEqual(tournament.status, "upcoming")

    def test_tournament_moves_to_ongoing_when_started(self):
        tournament = Tournament.objects.create(
            host=self.host,
            title="Ongoing Tournament",
            description="Currently running",
            game_type="web2",
            game_category="fps",
            start_date=timezone.now() - timedelta(hours=1),
            end_date=timezone.now() + timedelta(hours=1),
            is_approved=True
        )
        tournament.refresh_from_db()
        self.assertEqual(tournament.status, "ongoing")

    def test_tournament_moves_to_completed_when_ended(self):
        tournament = Tournament.objects.create(
            host=self.host,
            title="Completed Tournament",
            description="Already finished",
            game_type="web2",
            game_category="strategy",
            start_date=timezone.now() - timedelta(days=2),
            end_date=timezone.now() - timedelta(days=1),
            is_approved=True
        )
        tournament.refresh_from_db()
        self.assertEqual(tournament.status, "completed")

    def test_tournament_stays_pending_if_not_approved(self):
        tournament = Tournament.objects.create(
            host=self.host,
            title="Pending Tournament",
            description="Needs approval",
            game_type="web2",
            game_category="card",
            start_date=timezone.now() + timedelta(days=1),
            end_date=timezone.now() + timedelta(days=2),
            is_approved=False
        )
        tournament.refresh_from_db()
        self.assertEqual(tournament.status, "pending")

