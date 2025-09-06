from django.test import TestCase
from games.models import OddsScheme, GameConfig

class GameModelsTest(TestCase):
    def test_odds_scheme_creation(self):
        odds = OddsScheme.objects.create(
            bet_type="Pick-1",
            payout_multiplier=85.0,
            tax_rate=0.10
        )
        self.assertIsNotNone(odds.id)
        self.assertEqual(odds.bet_type, "Pick-1")
        self.assertEqual(float(odds.payout_multiplier), 85.0)
        self.assertEqual(float(odds.tax_rate), 0.10)

    def test_game_config_creation(self):
        odds = OddsScheme.objects.create(
            bet_type="Pick-1",
            payout_multiplier=85.0,
            tax_rate=0.10
        )
        game = GameConfig.objects.create(
            name="Test Game",
            range_min=1,
            range_max=99,
            draw_interval_sec=300,
            lock_offset_sec=60,
            min_bet=100,
            max_bet=10000,
            odds_scheme=odds
        )
        self.assertIsNotNone(game.id)
        self.assertEqual(game.name, "Test Game")
        self.assertEqual(game.odds_scheme, odds)