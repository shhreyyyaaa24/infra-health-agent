"""
Screenshot module using Playwright for dashboard captures
"""

import os
from playwright.sync_api import sync_playwright
from config import DASHBOARD_TAB_URLS, SCREENSHOT_DIR, SCREENSHOT_SELECTOR, SCREENSHOT_HEADLESS
from config.constants import DEFAULT_LOGIN_WAIT_TIME, AUTH_STATE_FILE


def ensure_screenshot_dir():
    """Create screenshot directory if it doesn't exist"""
    if not os.path.exists(SCREENSHOT_DIR):
        os.makedirs(SCREENSHOT_DIR)


def take_screenshots(login_mode=False):
    """Take screenshots of all dashboard URLs"""
    ensure_screenshot_dir()
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not login_mode)
        
        if login_mode:
            # Login mode: visible browser for manual authentication
            context = browser.new_context()
            page = context.new_page()
            
            print("Login mode: Please authenticate in the browser window...")
            print("After logging in, the browser will close automatically.")
            
            # Open first URL for login
            first_url = list(DASHBOARD_TAB_URLS.values())[0]
            page.goto(first_url)
            
            # Wait for user to complete login
            page.wait_for_timeout(DEFAULT_LOGIN_WAIT_TIME * 1000)  # Convert to milliseconds
            
            # Save auth state for future use
            context.storage_state(path=f"{SCREENSHOT_DIR}/{AUTH_STATE_FILE}")
            
        else:
            # Normal mode: use saved auth state if available
            auth_state_path = f"{SCREENSHOT_DIR}/{AUTH_STATE_FILE}"
            
            if os.path.exists(auth_state_path):
                context = browser.new_context(storage_state=auth_state_path)
            else:
                context = browser.new_context()
            
            screenshots_taken = []
            
            for env_name, url in DASHBOARD_TAB_URLS.items():
                page = context.new_page()
                
                try:
                    page.goto(url, wait_until="networkidle")
                    
                    # Wait for specific selector if configured
                    if SCREENSHOT_SELECTOR and SCREENSHOT_SELECTOR != "body":
                        page.wait_for_selector(SCREENSHOT_SELECTOR, timeout=10000)
                    
                    # Take screenshot
                    screenshot_path = f"{SCREENSHOT_DIR}/{env_name}_dashboard.png"
                    page.screenshot(path=screenshot_path, full_page=True)
                    screenshots_taken.append(screenshot_path)
                    
                    print(f"Screenshot saved: {screenshot_path}")
                    
                except Exception as e:
                    print(f"Failed to capture screenshot for {env_name}: {e}")
                    continue
                finally:
                    page.close()
            
            browser.close()
            return screenshots_taken


def login_and_save_state():
    """Open browser for manual login and save authentication state"""
    print("Starting login mode...")
    take_screenshots(login_mode=True)
    print("Login completed and authentication state saved.")


if __name__ == "__main__":
    # Test screenshot functionality
    take_screenshots()
