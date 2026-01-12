from django.db.models.signals import post_save
from django.dispatch import receiver
from authentication.models import ProofOfPayment
from authentication.utils import send_order_status_update


@receiver(post_save, sender=ProofOfPayment)
def send_proof_status_update(sender, instance, created, **kwargs):
    """
    Send email notification when proof of payment status changes (not on creation)
    """
    if not created:  # Only trigger when status is updated, not when first created
        if instance.order and instance.order.customer_email:
            try:
                send_order_status_update(
                    user_email=instance.order.customer_email,
                    order_id=instance.order.id,
                    new_status=instance.status
                )
            except Exception as email_error:
                print(f"Error sending proof status update email: {str(email_error)}")