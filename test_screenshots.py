#!/usr/bin/env python3
"""
Test screenshot embedding in email
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_screenshot_embedding():
    """Test that screenshots are properly embedded"""
    print("🖼️ Testing Screenshot Embedding\n")
    
    try:
        from data.fetcher import fetch_all_environment_data
        from email_module.email_composer import build_html_email
        
        # Get screenshot paths
        screenshot_paths = [
            "screenshots/gcp_dashboard.png",
            "screenshots/aws_dashboard.png", 
            "screenshots/azure_dashboard.png"
        ]
        
        print("📊 Fetching infrastructure data...")
        all_data = fetch_all_environment_data()
        
        print("📧 Building HTML email with screenshots...")
        html_body = build_html_email(all_data, screenshot_paths)
        
        # Check if screenshots are embedded
        checks = [
            ("📸 Dashboard Screenshots", "📸 Dashboard Screenshots" in html_body),
            ("GCP Dashboard", "GCP Dashboard" in html_body),
            ("AWS Dashboard", "AWS Dashboard" in html_body),
            ("Azure Dashboard", "Azure Dashboard" in html_body),
            ("data:image/png;base64", "data:image/png;base64" in html_body),
            ("iVBORw0K", "iVBORw0K" in html_body)  # PNG base64 signature
        ]
        
        print("\n🔍 Screenshot Embedding Checks:")
        for check_name, result in checks:
            status = "✅" if result else "❌"
            print(f"   {status} {check_name}")
        
        # Save email to check manually
        with open("test_screenshots_email.html", "w", encoding="utf-8") as f:
            f.write(html_body)
        
        print(f"\n💾 Email saved to: test_screenshots_email.html")
        print("📧 Open this file in a browser to see the screenshots")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_screenshot_embedding()
