#!/usr/bin/env python3
"""
Debug email content to see if it's being generated correctly
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def debug_full_email():
    """Debug the complete email content"""
    print("🔍 Debugging Complete Email Content\n")
    
    try:
        from data.fetcher import fetch_all_environment_data
        from email_module.email_composer import build_html_email, build_text_email
        
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
        
        print(f"📏 HTML email length: {len(html_body)} characters")
        
        # Save complete email for inspection
        with open("debug_complete_email.html", "w", encoding="utf-8") as f:
            f.write(html_body)
        
        print("💾 Complete HTML email saved to: debug_complete_email.html")
        
        # Build text email
        print("📧 Building text email...")
        text_body = build_text_email(all_data)
        
        print(f"📏 Text email length: {len(text_body)} characters")
        
        with open("debug_complete_email.txt", "w", encoding="utf-8") as f:
            f.write(text_body)
        
        print("💾 Complete text email saved to: debug_complete_email.txt")
        
        # Check for specific sections
        checks = [
            ("Hi Shreya Tiwari", "Hi Shreya Tiwari" in html_body),
            ("Status section", "Status" in html_body),
            ("Important Updates", "Important Updates" in html_body),
            ("Summary", "Summary" in html_body),
            ("Total Projects", "Total Projects" in html_body),
            ("Project Details", "Project Details" in html_body),
            ("table", "<table" in html_body),
            ("Screenshots", "Screenshots" in html_body),
            ("This report was generated", "This report was generated" in html_body)
        ]
        
        print("\n🔍 Content Section Checks:")
        for check_name, result in checks:
            status = "✅" if result else "❌"
            print(f"   {status} {check_name}")
        
        # Show last 200 characters to see if email is complete
        print(f"\n📝 Last 200 characters of HTML email:")
        print("=" * 50)
        print(html_body[-200:])
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ Debug failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    debug_full_email()
