from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from perfumes.models import Perfume, Order
from django.contrib.auth.models import User
from .models import ContactInfo, BankingDetails, ProofOfPayment
from .utils import send_proof_of_payment_confirmation


@staff_member_required
def admin_dashboard(request):
    """Admin dashboard page"""
    # Get or create contact info instance
    contact_info, created = ContactInfo.objects.get_or_create(
        id=1,
        defaults={
            'address': '123 Luxury Avenue',
            'city': 'New York',
            'state': 'NY',
            'zip_code': '10001',
            'email': 'contact@essence.com',
            'phone': '+1 (555) 123-4567',
        }
    )

    # Get some statistics for the dashboard
    total_perfumes = Perfume.objects.count()
    total_orders = Order.objects.count()
    total_users = User.objects.count()

    # Calculate developer's pay (5% of total order amounts after last payment, only for approved/shipped/delivered orders)
    from django.db.models import Sum
    from decimal import Decimal
    from .models import DeveloperPayment

    # Find the date of the most recent developer payment
    last_payment = DeveloperPayment.objects.order_by('-payment_date').first()

    # Only include orders with approved, shipped, or delivered status
    valid_statuses = ['approved', 'shipped', 'delivered']

    if last_payment:
        # Calculate developer's pay for orders created after the last payment with valid statuses
        total_order_amounts = Order.objects.filter(
            created_at__gt=last_payment.payment_date,
            status__in=valid_statuses
        ).aggregate(total=Sum('total'))['total'] or Decimal('0')
    else:
        # Calculate developer's pay for all orders with valid statuses (first time setup)
        total_order_amounts = Order.objects.filter(
            status__in=valid_statuses
        ).aggregate(total=Sum('total'))['total'] or Decimal('0')

    developers_pay = total_order_amounts * Decimal('0.05')

    recent_orders = Order.objects.order_by('-created_at')[:5]

    context = {
        'total_perfumes': total_perfumes,
        'total_orders': total_orders,
        'total_users': total_users,
        'developers_pay': developers_pay,
        'recent_orders': recent_orders,
        'title': 'Admin Dashboard',
        'contact_info': contact_info,
    }
    return render(request, 'admin_dashboard.html', context)


@staff_member_required
def edit_contact_info(request):
    """Edit contact information - accessible from admin dashboard"""
    contact_info, created = ContactInfo.objects.get_or_create(
        id=1,
        defaults={
            'address': '123 Luxury Avenue',
            'city': 'New York',
            'state': 'NY',
            'zip_code': '10001',
            'email': 'contact@essence.com',
            'phone': '+1 (555) 123-4567',
        }
    )

    if request.method == 'POST':
        contact_info.address = request.POST.get('address', contact_info.address)
        contact_info.city = request.POST.get('city', contact_info.city)
        contact_info.state = request.POST.get('state', contact_info.state)
        contact_info.zip_code = request.POST.get('zip_code', contact_info.zip_code)
        contact_info.email = request.POST.get('email', contact_info.email)
        contact_info.phone = request.POST.get('phone', contact_info.phone)

        try:
            contact_info.save()
            messages.success(request, 'Contact information updated successfully!')
            return redirect('admin_dashboard')
        except Exception as e:
            messages.error(request, f'Error updating contact information: {str(e)}')

    context = {
        'contact_info': contact_info,
        'title': 'Edit Contact Information'
    }
    return render(request, 'edit_contact_info.html', context)


def banking_details_page(request, order_id=None):
    """Banking details page for customers to make payment"""
    banking_details, created = BankingDetails.objects.get_or_create(
        id=1,
        defaults={
            'bank_name': 'Standard Bank',
            'account_holder_name': 'Essence Luxury Perfumes',
            'account_number': '0000000000',
            'branch_code': '000000',
            'branch_name': 'Sandton City',
            'swift_code': 'SBZAZAJJ',
            'reference_instruction': 'Use your order number as reference'
        }
    )

    # Get order if order_id is provided
    order = None
    proofs = None
    if order_id:
        try:
            from perfumes.models import Order
            order = Order.objects.get(id=order_id)
            # Get any existing proofs of payment for this order by the current user
            proofs = ProofOfPayment.objects.filter(order=order, user=request.user).order_by('-uploaded_at')
        except:
            order = None

    # Handle proof of payment upload
    if request.method == 'POST' and order and 'proof_upload' in request.FILES:
        proof_file = request.FILES['proof_upload']

        # Validate file type
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.pdf', '.doc', '.docx']
        file_extension = '.' + proof_file.name.lower().split('.')[-1]

        if file_extension in allowed_extensions:
            try:
                proof = ProofOfPayment.objects.create(
                    order=order,
                    user=request.user,
                    proof_image=proof_file if file_extension in ['.jpg', '.jpeg', '.png'] else None,
                    proof_document=proof_file if file_extension not in ['.jpg', '.jpeg', '.png'] else None
                )
                messages.success(request, 'Proof of payment uploaded successfully!')

                # Send email notification to customer
                try:
                    send_proof_of_payment_confirmation(
                        user_email=request.user.email,
                        order_id=order.id,
                        file_name=proof_file.name
                    )
                except Exception as email_error:
                    # Log the error but don't fail the upload if email sending fails
                    print(f"Error sending proof of payment confirmation email: {str(email_error)}")
            except Exception as e:
                messages.error(request, f'Error uploading proof of payment: {str(e)}')
        else:
            messages.error(request, 'Invalid file type. Please upload an image (JPG, PNG) or document (PDF, DOC).')

        # Redirect to prevent resubmission on refresh
        return redirect('banking_details', order_id=order.id)

    context = {
        'banking_details': banking_details,
        'order': order,
        'proofs': proofs,
        'title': 'Banking Details - Make Payment'
    }
    return render(request, 'banking_details.html', context)


@staff_member_required
def edit_banking_details(request):
    """Edit banking details - accessible from admin dashboard"""
    banking_details, created = BankingDetails.objects.get_or_create(
        id=1,
        defaults={
            'bank_name': 'Standard Bank',
            'account_holder_name': 'Essence Luxury Perfumes',
            'account_number': '0000000000',
            'branch_code': '000000',
            'branch_name': 'Sandton City',
            'swift_code': 'SBZAZAJJ',
            'reference_instruction': 'Use your order number as reference'
        }
    )

    if request.method == 'POST':
        banking_details.bank_name = request.POST.get('bank_name', banking_details.bank_name)
        banking_details.account_holder_name = request.POST.get('account_holder_name', banking_details.account_holder_name)
        banking_details.account_number = request.POST.get('account_number', banking_details.account_number)
        banking_details.branch_code = request.POST.get('branch_code', banking_details.branch_code)
        banking_details.branch_name = request.POST.get('branch_name', banking_details.branch_name)
        banking_details.swift_code = request.POST.get('swift_code', banking_details.swift_code)
        banking_details.reference_instruction = request.POST.get('reference_instruction', banking_details.reference_instruction)

        try:
            banking_details.save()
            messages.success(request, 'Banking details updated successfully!')
            return redirect('admin_dashboard')
        except Exception as e:
            messages.error(request, f'Error updating banking details: {str(e)}')

    context = {
        'banking_details': banking_details,
        'title': 'Edit Banking Details'
    }
    return render(request, 'edit_banking_details.html', context)


@staff_member_required
def developer_payment(request):
    """Page for making payment to developer"""
    from django.db.models import Sum
    from decimal import Decimal
    from django.contrib import messages
    from .utils import send_developer_payment_confirmation
    from .models import DeveloperPayment

    # Find the date of the most recent developer payment
    last_payment = DeveloperPayment.objects.order_by('-payment_date').first()

    # Only include orders with approved, shipped, or delivered status
    valid_statuses = ['approved', 'shipped', 'delivered']

    if last_payment:
        # Calculate developer's pay for orders created after the last payment with valid statuses
        total_order_amounts = Order.objects.filter(
            created_at__gt=last_payment.payment_date,
            status__in=valid_statuses
        ).aggregate(total=Sum('total'))['total'] or Decimal('0')
    else:
        # Calculate developer's pay for all orders with valid statuses (first time setup)
        total_order_amounts = Order.objects.filter(
            status__in=valid_statuses
        ).aggregate(total=Sum('total'))['total'] or Decimal('0')

    developers_pay = total_order_amounts * Decimal('0.05')

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')

        if not payment_method:
            messages.error(request, 'Please select a payment method.')
        elif payment_method not in ['eft', 'bobpay']:
            messages.error(request, 'Please select a valid payment method (EFT or BobPay).')
        elif payment_method == 'eft':
            # Handle EFT payment method
            proof_of_payment = request.FILES.get('proof_of_payment')
            payment_date = request.POST.get('payment_date')
            reference = request.POST.get('reference')

            # Validate required fields for EFT
            if not proof_of_payment:
                messages.error(request, 'Please upload a proof of payment file.')
            elif not payment_date:
                messages.error(request, 'Please enter the payment date.')
            elif not reference:
                messages.error(request, 'Please enter a reference number.')
            else:
                # Process the proof of payment
                try:
                    # Send email to developer with the proof of payment
                    send_developer_payment_confirmation(
                        developer_email='pontshokganakga863@gmail.com',
                        amount=developers_pay,
                        payment_date=payment_date,
                        reference=reference,
                        proof_file=proof_of_payment
                    )

                    # Save the payment record with the selected payment method
                    payment_record = DeveloperPayment.objects.create(
                        amount=developers_pay,
                        reference=reference,
                        payment_method=payment_method,
                        proof_of_payment=proof_of_payment
                    )

                    messages.success(request, f'Proof of payment uploaded and email sent to the developer successfully! Amount: R{developers_pay} via EFT/Swift Transfer')
                    # Redirect to prevent resubmission on refresh
                    return redirect('developer_payment')
                except Exception as e:
                    messages.error(request, f'Error sending email to developer: {str(e)}')
        elif payment_method == 'bobpay':
            # Handle BobPay payment method
            developer_email = request.POST.get('developer_email')
            card_number = request.POST.get('card_number')
            expiry_date = request.POST.get('expiry_date')
            cvv = request.POST.get('cvv')
            cardholder_name = request.POST.get('cardholder_name')
            payment_date = request.POST.get('payment_date', '')  # BobPay might not need this
            reference = request.POST.get('reference', f'BOBPAY-{int(developers_pay * 100)}')  # Generate reference for BobPay

            # Validate required fields for BobPay
            if not all([developer_email, card_number, expiry_date, cvv, cardholder_name]):
                messages.error(request, 'Please fill in all required payment details for BobPay.')
            else:
                # Process the BobPay payment
                try:
                    # In a real implementation, this would integrate with BobPay's API
                    # For now, we'll simulate a successful payment and send confirmation

                    # Send email to developer with payment details
                    send_developer_payment_confirmation(
                        developer_email=developer_email,
                        amount=developers_pay,
                        payment_date=payment_date or 'Today',
                        reference=reference,
                        proof_file=None  # No proof file for BobPay simulation
                    )

                    # Save the payment record with the selected payment method
                    payment_record = DeveloperPayment.objects.create(
                        amount=developers_pay,
                        reference=reference,
                        payment_method=payment_method
                        # For BobPay, we don't have a proof of payment file
                    )

                    messages.success(request, f'BobPay payment processed successfully! Amount: R{developers_pay} sent to developer via BobPay')
                    # Redirect to prevent resubmission on refresh
                    return redirect('developer_payment')
                except Exception as e:
                    messages.error(request, f'Error processing BobPay payment: {str(e)}')

    context = {
        'developers_pay': developers_pay,
        'title': 'Developer Payment',
    }
    return render(request, 'developer_payment.html', context)


def admin_login(request):
    """Admin login page - this can be accessed from the main auth page"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials or you do not have admin access.')
    
    return render(request, 'admin_login.html')