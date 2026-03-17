#!/usr/bin/env python3
"""
Debug email content to see what's being sent
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def debug_email_content():
    """Debug the email content to see what's being generated"""
    print("🔍 Debugging Email Content\n")
    
    try:
        # Import modules
        from data.fetcher import fetch_all_environment_data
        from email_module.email_composer import build_html_email
        
        print("📊 Fetching infrastructure data...")
        all_data = fetch_all_environment_data()
        
        if not all_data:
            print("❌ No data fetched")
            return False
        
        print(f"✅ Data fetched: {len(all_data)} environments")
        for env, projects in all_data.items():
            print(f"   {env}: {len(projects)} projects")
        
        print("\n📧 Building HTML email...")
        html_body = build_html_email(all_data)
        
        print(f"📏 Email HTML length: {len(html_body)} characters")
        
        # Save email content to file for inspection
        with open("debug_email.html", "w", encoding="utf-8") as f:
            f.write(html_body)
        
        print("💾 Email content saved to: debug_email.html")
        
        # Show first 500 characters
        print("\n📝 First 500 characters of email:")
        print("=" * 50)
        print(html_body[:500])
        print("=" * 50)
        
        # Check if email contains expected content
        checks = [
            ("Hi Shreya", "Hi Shreya" in html_body),
            ("Infrastructure Status Summary", "Infrastructure Status Summary" in html_body),
            ("Total Projects", "Total Projects" in html_body),
            ("Project Details", "Project Details" in html_body),
            ("<table", "<table" in html_body),
            ("</html>", "</html>" in html_body)
        ]
        
        print("\n🔍 Content Checks:")
        for check_name, result in checks:
            status = "✅" if result else "❌"
            print(f"   {status} {check_name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Debug failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    debug_email_content()
