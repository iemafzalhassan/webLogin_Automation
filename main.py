import time
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        # Launch a browser (Chromium in this case)
        browser = p.chromium.launch(headless=False, slow_mo=50)  # headless=False to see the browser action
        page = browser.new_page()

        # Go to the Suno website
        page.goto('https://suno.com', wait_until='domcontentloaded')

        # Wait for the "Sign In" button and click it
        try:
            sign_in_button = page.wait_for_selector('button.group.font-medium.text-sm.flex.flex-row.flex-nowrap.items-center.justify-center.select-none', timeout=60000)
            print("Sign In button found. Clicking...")
            sign_in_button.click()
        except Exception as e:
            print(f"Error: Could not find 'Sign In' button within timeout: {e}")
            browser.close()
            return

        # Wait for the "Login with Google" button and click it
        try:
            google_login_button = page.wait_for_selector('button.cl-socialButtonsIconButton:nth-child(3)', timeout=60000)
            print("Login with Google button found. Clicking...")
            google_login_button.click()
        except Exception as e:
            print(f"Error: Could not find Google login button within timeout: {e}")
            browser.close()
            return

        # Wait for the Google login page to load
        page.wait_for_navigation(wait_until='networkidle')

        # Handle Google login (email and password)
        try:
            # Wait for the email field and type email
            page.wait_for_selector('input[type="email"]')
            page.fill('input[type="email"]', 'your_email@gmail.com')  # Replace with your email
            page.click('#identifierNext')

            # Wait for password input field and type password
            page.wait_for_selector('input[type="password"]')
            page.fill('input[type="password"]', 'your_password')  # Replace with your password
            page.click('#passwordNext')

        except Exception as e:
            print(f"Error: Issue with Google login: {e}")
            browser.close()
            return

        # Handle CAPTCHA or 2FA if they appear
        try:
            page.wait_for_selector('#yDmH0d', timeout=10000)  # Timeout after 10 seconds if CAPTCHA or 2FA appears
            print("2FA or CAPTCHA required, manual intervention needed.")
            time.sleep(60)  # Wait for user to solve CAPTCHA/2FA manually
        except Exception:
            print("Login successful, no extra steps needed.")

        # Wait for the page to load after successful login
        page.wait_for_selector('body')  # Wait for the body of the page to ensure everything is loaded

        # Optionally close the browser
        # browser.close()

if __name__ == "__main__":
    run()

