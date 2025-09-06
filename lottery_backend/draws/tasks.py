from celery import shared_task
from django.utils import timezone
from .models import Draw
from games.models import GameConfig
from payouts.tasks import payout_winners
import hashlib
import hmac
import os

@shared_task
def schedule_draws():
    game_configs = GameConfig.objects.all()
    for config in game_configs:
        # Calculate the next scheduled draw time
        now = timezone.now()
        # This is a simplified logic. In a real scenario, you would calculate
        # the next draw time based on the last draw and interval.
        scheduled_at = now + timezone.timedelta(seconds=config.draw_interval_sec)
        locked_at = scheduled_at - timezone.timedelta(seconds=config.lock_offset_sec)

        # Generate seed commit hash and seed reveal
        seed_reveal = os.urandom(32).hex()
        seed_commit_hash = hashlib.sha256(seed_reveal.encode()).hexdigest()
        print("Seed Reveal:", seed_reveal)
        print("Seed Commit Hash:", seed_commit_hash)
        draw, created = Draw.objects.get_or_create(
            game=config,
            scheduled_at=scheduled_at,
            defaults={
                'locked_at': locked_at,
                'seed_commit_hash': seed_commit_hash,
                'status': Draw.DrawStatus.PENDING
            }
        )

        if created:
            print(f"Scheduled new draw for {config.name} at {scheduled_at}")
            # Dynamically schedule lock_draw and execute_draw
            lock_draw.apply_async((draw.id,), eta=draw.locked_at)
            execute_draw.apply_async((draw.id, seed_reveal), eta=draw.scheduled_at)
        else:
            print(f"Draw for {config.name} at {scheduled_at} already exists.")

@shared_task
def execute_draw(draw_id, seed_reveal):
    try:
        draw = Draw.objects.get(id=draw_id)
    except Draw.DoesNotExist:
        print(f"Draw with ID {draw_id} not found.")
        return

    if draw.status != Draw.DrawStatus.CLOSED:
        print(f"Draw {draw_id} is not in CLOSED status. Current status: {draw.status}")
        return

    # Generate winning number using HMAC and seed_reveal
    # The nonce can be a combination of draw ID and scheduled time for uniqueness
    draw_nonce = f"{draw.id}-{draw.scheduled_at.timestamp()}"
    winning_number = (int(hmac.new(seed_reveal.encode(), draw_nonce.encode(), hashlib.sha256).hexdigest(), 16) % (draw.game.range_max - draw.game.range_min + 1)) + draw.game.range_min

    draw.winning_number = winning_number
    draw.seed_reveal = seed_reveal
    draw.status = Draw.DrawStatus.RESULTED
    draw.save()

    print(f"Executed draw {draw_id}. Winning number: {winning_number}")

    # Trigger payout task
    payout_winners.delay(draw_id)

@shared_task
def lock_draw(draw_id):
    try:
        draw = Draw.objects.get(id=draw_id)
    except Draw.DoesNotExist:
        print(f"Draw with ID {draw_id} not found.")
        return

    if draw.status == Draw.DrawStatus.PENDING:
        draw.status = Draw.DrawStatus.CLOSED
        draw.save()
        print(f"Locked draw {draw_id}.")
    else:
        print(f"Draw {draw_id} is not in PENDING status. Current status: {draw.status}")
