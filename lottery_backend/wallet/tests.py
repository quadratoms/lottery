from django.test import TestCase
from django.contrib.auth import get_user_model
from wallet.models import Wallet, LedgerEntry
from payments.models import Payment
from payouts.models import Payout
from tickets.models import Ticket
from draws.models import Draw
from games.models import GameConfig, OddsScheme
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta
from django.db import transaction

User = get_user_model()

class WalletModelsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        self.wallet = Wallet.objects.create(user=self.user, available=Decimal('1000.00'), locked=Decimal('0.00'))
        self.odds_scheme = OddsScheme.objects.create(
            bet_type="Pick-1",
            payout_multiplier=Decimal('85.0'),
            tax_rate=Decimal('0.10')
        )
        self.game_config = GameConfig.objects.create(
            name="Test Lottery",
            range_min=1,
            range_max=99,
            draw_interval_sec=300,
            lock_offset_sec=60,
            min_bet=100,
            max_bet=10000,
            odds_scheme=self.odds_scheme
        )
        self.draw = Draw.objects.create(
            game=self.game_config,
            scheduled_at=timezone.now() + timedelta(minutes=10),
            locked_at=timezone.now() + timedelta(minutes=5),
            seed_commit_hash="test_commit_hash",
            seed_reveal="test_seed_reveal",
            status=Draw.DrawStatus.PENDING
        )

    def test_wallet_creation(self):
        self.assertIsNotNone(self.wallet.id)
        self.assertEqual(self.wallet.user, self.user)
        self.assertEqual(self.wallet.available, Decimal('1000.00'))
        self.assertEqual(self.wallet.locked, Decimal('0.00'))

    def test_ledger_entry_creation(self):
        entry = LedgerEntry.objects.create(
            wallet=self.wallet,
            type='DEPOSIT',
            amount=Decimal('500.00'),
            balance_after=Decimal('1500.00'),
            ref='deposit_ref_1',
            meta={'source': 'test'}
        )
        self.assertIsNotNone(entry.id)
        self.assertEqual(entry.wallet, self.wallet)
        self.assertEqual(entry.type, 'DEPOSIT')
        self.assertEqual(entry.amount, Decimal('500.00'))
        self.assertEqual(entry.balance_after, Decimal('1500.00'))

    def test_deposit_updates_wallet_and_ledger(self):
        initial_balance = self.wallet.available
        deposit_amount = Decimal('200.00')

        # Simulate successful payment processing
        payment = Payment.objects.create(
            user=self.user,
            type=Payment.PaymentType.DEPOSIT,
            provider="TestProvider",
            amount=deposit_amount,
            status=Payment.PaymentStatus.SUCCESS
        )

        with transaction.atomic():
            wallet = Wallet.objects.select_for_update().get(user=self.user)
            wallet.available += deposit_amount
            wallet.save()

            LedgerEntry.objects.create(
                wallet=wallet,
                type='DEPOSIT',
                amount=deposit_amount,
                balance_after=wallet.available,
                ref=f'payment_{payment.id}',
                meta={'payment_id': payment.id}
            )

        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.available, initial_balance + deposit_amount)
        self.assertEqual(LedgerEntry.objects.filter(wallet=self.wallet, type='DEPOSIT').count(), 1)

    def test_bet_placement_updates_wallet_and_ledger(self):
        initial_available = self.wallet.available
        initial_locked = self.wallet.locked
        stake = Decimal('100.00')

        ticket = Ticket.objects.create(
            user=self.user,
            draw=self.draw,
            selection=50,
            stake=stake,
            potential_payout=stake * self.odds_scheme.payout_multiplier,
            ticket_hash="test_ticket_hash"
        )

        with transaction.atomic():
            wallet = Wallet.objects.select_for_update().get(user=self.user)
            wallet.available -= stake
            wallet.locked += stake
            wallet.save()

            LedgerEntry.objects.create(
                wallet=wallet,
                type='BET_PLACE',
                amount=stake,
                balance_after=wallet.available,
                ref=f'ticket_{ticket.id}',
                meta={'ticket_id': ticket.id}
            )

        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.available, initial_available - stake)
        self.assertEqual(self.wallet.locked, initial_locked + stake)
        self.assertEqual(LedgerEntry.objects.filter(wallet=self.wallet, type='BET_PLACE').count(), 1)

    def test_payout_updates_wallet_and_ledger(self):
        # First, simulate a bet placement
        stake = Decimal('100.00')
        potential_payout = stake * self.odds_scheme.payout_multiplier
        tax_withheld = potential_payout * self.odds_scheme.tax_rate
        actual_payout = potential_payout - tax_withheld

        ticket = Ticket.objects.create(
            user=self.user,
            draw=self.draw,
            selection=50,
            stake=stake,
            potential_payout=potential_payout,
            ticket_hash="test_ticket_hash",
            status=Ticket.TicketStatus.WON
        )

        # Simulate locking funds for the bet
        with transaction.atomic():
            wallet = Wallet.objects.select_for_update().get(user=self.user)
            wallet.available -= stake
            wallet.locked += stake
            wallet.save()
        self.wallet.refresh_from_db() # Refresh wallet state after bet placement
        initial_available = self.wallet.available
        initial_locked = self.wallet.locked

        # Now, simulate payout
        Payout.objects.create(
            ticket=ticket,
            amount=actual_payout,
            tax_withheld=tax_withheld,
            status=Payout.PayoutStatus.SUCCESS
        )

        with transaction.atomic():
            wallet = Wallet.objects.select_for_update().get(user=self.user)
            wallet.available += actual_payout
            wallet.locked -= stake # Release locked funds
            wallet.save()

            LedgerEntry.objects.create(
                wallet=wallet,
                type='WIN_PAYOUT',
                amount=actual_payout,
                balance_after=wallet.available,
                ref=f'payout_{ticket.id}',
                meta={'ticket_id': ticket.id}
            )

        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.available, initial_available + actual_payout)
        self.assertEqual(self.wallet.locked, initial_locked - stake)
        self.assertEqual(LedgerEntry.objects.filter(wallet=self.wallet, type='WIN_PAYOUT').count(), 1)

    def test_losing_ticket_releases_locked_funds(self):
        stake = Decimal('100.00')
        ticket = Ticket.objects.create(
            user=self.user,
            draw=self.draw,
            selection=50,
            stake=stake,
            potential_payout=Decimal('0.00'),
            ticket_hash="test_ticket_hash",
            status=Ticket.TicketStatus.LOST
        )

        # Simulate locking funds for the bet
        with transaction.atomic():
            wallet = Wallet.objects.select_for_update().get(user=self.user)
            wallet.available -= stake
            wallet.locked += stake
            wallet.save()
        self.wallet.refresh_from_db() # Refresh wallet state after bet placement
        initial_available = self.wallet.available
        initial_locked = self.wallet.locked

        # Simulate releasing locked funds for losing ticket
        with transaction.atomic():
            wallet = Wallet.objects.select_for_update().get(user=self.user)
            wallet.locked -= stake
            wallet.save()

        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.available, initial_available)
        self.assertEqual(self.wallet.locked, initial_locked - stake)