from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from draws.models import Draw
from games.models import GameConfig, OddsScheme
from draws.tasks import schedule_draws, execute_draw
import hashlib
import hmac

class DrawTasksTest(TestCase):
    def setUp(self):
        self.odds_scheme = OddsScheme.objects.create(
            bet_type="Pick-1",
            payout_multiplier=85.0,
            tax_rate=0.10
        )
        self.game_config = GameConfig.objects.create(
            name="Test Lottery",
            range_min=1,
            range_max=99,
            draw_interval_sec=300, # 5 minutes
            lock_offset_sec=60, # 1 minute
            min_bet=100,
            max_bet=10000,
            odds_scheme=self.odds_scheme
        )

    def test_schedule_draws(self):
        initial_draw_count = Draw.objects.count()
        schedule_draws()
        self.assertEqual(Draw.objects.count(), initial_draw_count + 1)
        draw = Draw.objects.latest('id')
        self.assertEqual(draw.game, self.game_config)
        self.assertEqual(draw.status, Draw.DrawStatus.PENDING)
        self.assertIsNotNone(draw.seed_commit_hash)
        self.assertIsNotNone(draw.seed_reveal)

    def test_execute_draw(self):
        # Schedule a draw first
        schedule_draws()
        draw = Draw.objects.latest('id')

        # Execute the draw
        execute_draw(draw.id)

        draw.refresh_from_db()
        self.assertEqual(draw.status, Draw.DrawStatus.RESULTED)
        self.assertIsNotNone(draw.winning_number)
        self.assertTrue(self.game_config.range_min <= draw.winning_number <= self.game_config.range_max)

        # Verify commit-reveal
        draw_nonce = f"{draw.id}-{draw.scheduled_at.timestamp()}"
        expected_winning_number = (int(hmac.new(draw.seed_reveal.encode(), draw_nonce.encode(), hashlib.sha256).hexdigest(), 16) % (draw.game.range_max - draw.game.range_min + 1)) + draw.game.range_min
        self.assertEqual(draw.winning_number, expected_winning_number)

        # Ensure seed_commit_hash matches revealed seed
        self.assertEqual(draw.seed_commit_hash, hashlib.sha256(draw.seed_reveal.encode()).hexdigest())