#!/usr/bin/env python3
"""
Test the main email sending function directly
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_main_email_function():
    """Test the main email function directly"""
    print("🔧 Testing Main Email Function\n")
    
    try:
        from data.fetcher import fetch_all_environment_data
        from email_module.email_composer import build_html_email
        from email_module.mailer import send_email_with_attachments
        
        print("📊 Fetching infrastructure data...")
        all_data = fetch_all_environment_data()
        
        if not all_data:
            print("❌ No data fetched")
            return False
        
        print(f"✅ Data fetched: {len(all_data)} environments")
        
        # Get screenshot paths
        screenshot_paths = [
            "screenshots/gcp_shreya_component_1.png",
            "screenshots/aws_shreya_component_1.png", 
            "screenshots/azure_shreya_component_1.png"
        ]
        
        print("📧 Building HTML email...")
        html_body = build_html_email(all_data, screenshot_paths)
        
        print(f"📏 HTML body length: {len(html_body)} characters")
        
        # Show first 500 characters
        print(f"\n📝 First 500 characters:")
        print("=" * 50)
        print(html_body[:500])
        print("=" * 50)
        
        # Show last 200 characters
        print(f"\n📝 Last 200 characters:")
        print("=" * 50)
        print(html_body[-200:])
        print("=" * 50)
        
        print("\n📧 Sending email via main function...")
        success = send_email_with_attachments(html_body, screenshot_paths, all_data=all_data)
        
        if success:
            print("✅ Main email function sent successfully!")
        else:
            print("❌ Main email function failed")
        
        return success
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_main_email_function()
