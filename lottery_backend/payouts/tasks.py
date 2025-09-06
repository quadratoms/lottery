from celery import shared_task
from django.db import transaction

from draws.models import Draw
from .models import Payout
from tickets.models import Ticket
from wallet.models import Wallet, LedgerEntry

@shared_task
def payout_winners(draw_id):
    try:
        draw = Draw.objects.get(id=draw_id)
    except Draw.DoesNotExist:
        print(f"Draw with ID {draw_id} not found.")
        return

    if draw.status != Draw.DrawStatus.RESULTED:
        print(f"Draw {draw_id} is not in RESULTED status. Current status: {draw.status}")
        return

    tickets = Ticket.objects.filter(draw=draw)

    for ticket in tickets:
        if ticket.selection == draw.winning_number:
            # Winning ticket
            with transaction.atomic():
                try:
                    wallet = Wallet.objects.select_for_update().get(user=ticket.user)
                    
                    # Calculate payout amount based on the odds scheme
                    payout_amount = ticket.potential_payout
                    
                    wallet.available += payout_amount
                    wallet.save()

                    # Create a ledger entry for the payout
                    LedgerEntry.objects.create(
                        wallet=wallet,
                        type='WIN_PAYOUT',
                        amount=payout_amount,
                        balance_after=wallet.available,
                        ref=f"ticket-{ticket.id}"
                    )

                    ticket.status = Ticket.TicketStatus.WON
                    ticket.save()

                    print(f"Paid out ticket {ticket.id}. Amount: {payout_amount}")

                except Wallet.DoesNotExist:
                    print(f"Wallet for user {ticket.user.id} not found.")
                except Exception as e:
                    print(f"Error processing payout for ticket {ticket.id}: {e}")
        else:
            # Losing ticket
            ticket.status = Ticket.TicketStatus.LOST
            ticket.save()
            print(f"Marked ticket {ticket.id} as LOST.")
