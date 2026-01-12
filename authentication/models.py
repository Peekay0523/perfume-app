from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


class ContactInfo(models.Model):
    address = models.CharField(max_length=255, default='123 Luxury Avenue')
    city = models.CharField(max_length=100, default='New York')
    state = models.CharField(max_length=100, default='NY')
    zip_code = models.CharField(max_length=20, default='10001')
    email = models.EmailField(default='contact@essence.com')
    phone = models.CharField(max_length=20, default='+1 (555) 123-4567')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Contact Information'
        verbose_name_plural = 'Contact Information'

    def __str__(self):
        return f"Contact Info - {self.email}"


class BankingDetails(models.Model):
    bank_name = models.CharField(max_length=100, default='Standard Bank')
    account_holder_name = models.CharField(max_length=255, default='Essence Luxury Perfumes')
    account_number = models.CharField(max_length=50, default='0000000000')
    branch_code = models.CharField(max_length=20, default='000000')
    branch_name = models.CharField(max_length=100, default='Sandton City')
    swift_code = models.CharField(max_length=20, default='SBZAZAJJ', null=True, blank=True)
    reference_instruction = models.TextField(default="Use your order number as reference", blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Banking Details'
        verbose_name_plural = 'Banking Details'

    def __str__(self):
        return f"Banking Details - {self.bank_name}"


class ProofOfPayment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('rejected', 'Rejected'),
    ]

    order = models.ForeignKey('perfumes.Order', on_delete=models.CASCADE, related_name='proofs_of_payment')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    proof_image = models.ImageField(upload_to='proof_of_payment/', null=True, blank=True)
    proof_document = models.FileField(upload_to='proof_of_payment/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Proof of Payment'
        verbose_name_plural = 'Proof of Payments'

    def __str__(self):
        return f"Proof of Payment for Order #{self.order.id} - {self.user.username}"


class DeveloperPayment(models.Model):
    """Model to track developer payments"""
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Amount paid to developer")
    payment_date = models.DateTimeField(auto_now_add=True, help_text="Date when payment was recorded")
    reference = models.CharField(max_length=255, help_text="Payment reference number")
    proof_of_payment = models.FileField(upload_to='developer_payments/', null=True, blank=True, help_text="Proof of payment file")

    # Track orders included in this payment
    orders_included = models.TextField(help_text="Serialized list of order IDs included in this payment", blank=True)
    processed = models.BooleanField(default=False, help_text="Whether payment has been processed externally")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Developer Payment - R{self.amount} - {self.payment_date.strftime('%Y-%m-%d')}"