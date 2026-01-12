from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import logging


# Set up logger
logger = logging.getLogger(__name__)


def send_proof_of_payment_confirmation(user_email, order_id, file_name):
    """Send email confirmation when proof of payment is uploaded"""
    subject = f'Proof of Payment Received - Order #{order_id}'

    context = {
        'order_id': order_id,
        'file_name': file_name,
        'status': 'pending verification',
        'site_name': 'Essence Luxury Perfumes'
    }

    html_message = render_to_string('emails/proof_of_payment_confirmation.html', context)
    plain_message = strip_tags(html_message)

    try:
        result = send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            html_message=html_message,
            fail_silently=False,
        )

        # Log successful email sending
        logger.info(f"Proof of payment confirmation email sent successfully to {user_email} for order #{order_id}")
        return result
    except Exception as e:
        # Log email sending failure
        logger.error(f"Failed to send proof of payment confirmation email to {user_email} for order #{order_id}: {str(e)}")
        raise


def send_order_status_update(user_email, order_id, new_status):
    """Send email when order status changes"""
    subject = f'Order #{order_id} Status Update - {new_status.replace("_", " ").title()}'

    context = {
        'order_id': order_id,
        'new_status': new_status.replace("_", " ").title(),
        'site_name': 'Essence Luxury Perfumes'
    }

    html_message = render_to_string('emails/order_status_update.html', context)
    plain_message = strip_tags(html_message)

    try:
        result = send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            html_message=html_message,
            fail_silently=False,
        )

        # Log successful email sending
        logger.info(f"Order status update email sent successfully to {user_email} for order #{order_id}, new status: {new_status}")
        return result
    except Exception as e:
        # Log email sending failure
        logger.error(f"Failed to send order status update email to {user_email} for order #{order_id}, status: {new_status}: {str(e)}")
        raise


def send_developer_payment_confirmation(developer_email, amount, payment_date, reference, proof_file=None):
    """Send email with proof of payment to developer"""
    subject = f'Developer Payment Confirmation - R{amount}'

    context = {
        'amount': amount,
        'payment_date': payment_date,
        'reference': reference,
        'site_name': 'Essence Luxury Perfumes',
        'developer_name': 'Pontsho Kganakga'
    }

    html_message = render_to_string('emails/developer_payment_confirmation.html', context)
    plain_message = strip_tags(html_message)

    try:
        # Prepare email with attachment if provided
        if proof_file:
            from django.core.mail import EmailMultiAlternatives
            msg = EmailMultiAlternatives(
                subject=subject,
                body=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[developer_email]
            )
            msg.attach_alternative(html_message, "text/html")

            # Attach the proof of payment file
            msg.attach(proof_file.name, proof_file.read(), proof_file.content_type)

            result = msg.send()
        else:
            result = send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[developer_email],
                html_message=html_message,
                fail_silently=False,
            )

        # Log successful email sending
        logger.info(f"Developer payment confirmation email sent successfully to {developer_email}")
        return result
    except Exception as e:
        # Log email sending failure
        logger.error(f"Failed to send developer payment confirmation email to {developer_email}: {str(e)}")
        raise