#!/usr/bin/env python3
"""
Test email sending with infrastructure data
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_infrastructure_email():
    """Test sending infrastructure data via email"""
    print("🚀 Testing Infrastructure Email Sending\n")
    
    try:
        # Import modules
        from data.fetcher import fetch_all_environment_data
        from email_module.email_composer import build_html_email
        from email_module.mailer import send_email_with_attachments
        
        print("📊 Fetching infrastructure data...")
        all_data = fetch_all_environment_data()
        
        if not all_data:
            print("❌ No data fetched")
            return False
        
        print(f"✅ Data fetched: {len(all_data)} environments")
        
        print("📧 Building HTML email...")
        html_body = build_html_email(all_data)
        
        print("📨 Sending email...")
        success = send_email_with_attachments(html_body, screenshot_paths=None, dry_run=False)
        
        if success:
            print("✅ Infrastructure email sent successfully!")
            return True
        else:
            print("❌ Email sending failed")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_infrastructure_email()
