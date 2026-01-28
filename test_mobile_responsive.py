import requests
from bs4 import BeautifulSoup

def test_admin_orders_page():
    """
    Test the admin orders page to ensure it's mobile-friendly
    """
    # Test URL - adjust if needed based on your setup
    url = "http://127.0.0.1:8000/admin/orders/"
    
    # Since this requires admin access, we'll just check if the page loads
    try:
        # First, try to access the admin login page to understand the flow
        login_url = "http://127.0.0.1:8000/admin/login/"
        response = requests.get(login_url)
        
        if response.status_code == 200:
            print("Login page accessible")
        else:
            print(f"Login page not accessible, status code: {response.status_code}")
            
        # Check if the page contains mobile-friendly elements
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for viewport meta tag
        viewport_tag = soup.find('meta', attrs={'name': 'viewport'})
        if viewport_tag:
            print("[PASS] Viewport meta tag found - good for mobile")
        else:
            print("[FAIL] Viewport meta tag not found")
            
        # Check for responsive classes in the HTML
        # Since we can't access the protected admin page without credentials,
        # we'll just verify that the base template has responsive features
        
        print("\nNote: To fully test the admin orders page, you need to:")
        print("1. Log in to the admin panel with valid credentials")
        print("2. Navigate to the admin orders page")
        print("3. Test the page on different screen sizes")
        print("4. Verify that the table scrolls horizontally on small screens")
        
    except requests.exceptions.RequestException as e:
        print(f"Error accessing the page: {e}")

if __name__ == "__main__":
    test_admin_orders_page()