from .models import ContactInfo


def contact_info(request):
    """
    Context processor to make contact information available in all templates
    """
    try:
        contact_info_instance = ContactInfo.objects.first()
        if contact_info_instance is None:
            # Create a default instance if it doesn't exist
            contact_info_instance = ContactInfo.objects.create(
                address='123 Luxury Avenue',
                city='New York',
                state='NY',
                zip_code='10001',
                email='contact@essence.com',
                phone='+1 (555) 123-4567'
            )
        return {'contact_info': contact_info_instance}
    except:
        # If there's an error, return empty contact info to avoid breaking the site
        return {
            'contact_info': {
                'address': '123 Luxury Avenue',
                'city': 'New York',
                'state': 'NY',
                'zip_code': '10001',
                'email': 'contact@essence.com',
                'phone': '+1 (555) 123-4567'
            }
        }