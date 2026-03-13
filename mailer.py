"""
Generic email sending module using configurable providers
"""

import os
from email_composer import build_html_email, get_email_subject
from config import EMAIL_PROVIDER, EMAIL_CONFIG, DIRECTOR_CONFIG
from email_providers import get_email_provider


def send_email_with_attachments(html_body, screenshot_paths=None, dry_run=False):
    """Send email using configured provider with inline image attachments"""
    try:
        # Get email provider based on configuration
        provider_config = EMAIL_CONFIG[EMAIL_PROVIDER]
        email_provider = get_email_provider(EMAIL_PROVIDER, provider_config)
        
        # Send email using the provider
        return email_provider.send_email(html_body, screenshot_paths, dry_run)
        
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False


def preview_email_html(all_data, screenshot_paths=None):
    """Preview email HTML content using configured provider"""
    try:
        # Get email provider based on configuration
        provider_config = EMAIL_CONFIG[EMAIL_PROVIDER]
        email_provider = get_email_provider(EMAIL_PROVIDER, provider_config)
        
        # Build HTML and preview using the provider
        html_body = build_html_email(all_data, screenshot_paths)
        return email_provider.preview_email(html_body, screenshot_paths)
        
    except Exception as e:
        print(f"Failed to preview email: {e}")
        return None


if __name__ == "__main__":
    # Test email functionality
    from fetcher import fetch_all_environment_data
    
    print("Fetching data...")
    all_data = fetch_all_environment_data()
    
    print("Building email...")
    html_body = build_html_email(all_data)
    
    print("Previewing email...")
    preview_email_html(all_data)
