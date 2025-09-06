from django.core.management.base import BaseCommand
from games.models import GameConfig, OddsScheme
from draws.tasks import schedule_draws
from decimal import Decimal

class Command(BaseCommand):
    help = 'Seeds the database with default game configurations and initial draws.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Seeding default game configurations...'))

        # Create default OddsScheme
        odds_scheme, created = OddsScheme.objects.get_or_create(
            bet_type="Pick-1",
            defaults={
                'payout_multiplier': Decimal('85.0'),
                'tax_rate': Decimal('0.10')
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created default Pick-1 OddsScheme.'))
        else:
            self.stdout.write(self.style.SUCCESS('Pick-1 OddsScheme already exists.'))

        # Create default GameConfig
        game_config, created = GameConfig.objects.get_or_create(
            name="Daily Lottery (1-99)",
            defaults={
                'range_min': 1,
                'range_max': 99,
                'draw_interval_sec': 300, # 5 minutes
                'lock_offset_sec': 60, # 1 minute
                'min_bet': Decimal('100.00'),
                'max_bet': Decimal('10000.00'),
                'odds_scheme': odds_scheme
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created default Daily Lottery GameConfig.'))
        else:
            self.stdout.write(self.style.SUCCESS('Daily Lottery GameConfig already exists.'))

        # Schedule initial draws
        self.stdout.write(self.style.SUCCESS('Scheduling initial draws...'))
        schedule_draws()
        self.stdout.write(self.style.SUCCESS('Initial draws scheduled.'))

        self.stdout.write(self.style.SUCCESS('Seeding complete.'))
