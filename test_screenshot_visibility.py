#!/usr/bin/env python3
"""
Test if screenshots are actually visible in the email
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_screenshot_visibility():
    """Test if screenshots are properly embedded and visible"""
    print("🔍 Testing Screenshot Visibility\n")
    
    try:
        # Check if screenshot files exist and are readable
        screenshot_files = [
            "screenshots/gcp_dashboard.png",
            "screenshots/aws_dashboard.png", 
            "screenshots/azure_dashboard.png"
        ]
        
        print("📁 Checking screenshot files:")
        for screenshot_file in screenshot_files:
            if os.path.exists(screenshot_file):
                size = os.path.getsize(screenshot_file)
                print(f"   ✅ {screenshot_file} ({size} bytes)")
            else:
                print(f"   ❌ {screenshot_file} - Not found")
        
        # Test base64 conversion
        import base64
        print("\n🔄 Testing base64 conversion:")
        for screenshot_file in screenshot_files:
            if os.path.exists(screenshot_file):
                try:
                    with open(screenshot_file, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode('utf-8')
                    print(f"   ✅ {screenshot_file} - Base64 conversion successful ({len(image_data)} chars)")
                    
                    # Check if it starts with PNG signature
                    if image_data.startswith('iVBORw0K'):
                        print(f"      ✅ Valid PNG data")
                    else:
                        print(f"      ❌ Invalid PNG data")
                        
                except Exception as e:
                    print(f"   ❌ {screenshot_file} - Base64 conversion failed: {e}")
        
        # Test actual email content
        from data.fetcher import fetch_all_environment_data
        from email_module.email_composer import build_html_email
        
        print("\n📧 Testing email content:")
        all_data = fetch_all_environment_data()
        screenshot_paths = screenshot_files
        
        html_content = build_html_email(all_data, screenshot_paths)
        
        # Count base64 images
        base64_count = html_content.count('data:image/png;base64,')
        print(f"   📊 Base64 images found: {base64_count}")
        
        # Check for specific dashboard sections
        dashboards = ['GCP Dashboard', 'AWS Dashboard', 'AZURE Dashboard']
        for dashboard in dashboards:
            if dashboard in html_content:
                print(f"   ✅ {dashboard} section found")
            else:
                print(f"   ❌ {dashboard} section missing")
        
        # Save a simplified test email
        test_html = f"""
        <!DOCTYPE html>
        <html>
        <body>
            <h2>Screenshot Test</h2>
        """
        
        for screenshot_file in screenshot_files:
            if os.path.exists(screenshot_file):
                env_name = os.path.basename(screenshot_file).replace('_dashboard.png', '').upper()
                with open(screenshot_file, "rb") as image_file:
                    image_data = base64.b64encode(image_file.read()).decode('utf-8')
                
                test_html += f"""
                <div style="border: 2px solid red; margin: 10px; padding: 10px;">
                    <h3>{env_name} Dashboard</h3>
                    <img src="data:image/png;base64,{image_data}" style="max-width: 300px; border: 1px solid black;">
                    <p>If you can see this image, screenshots are working!</p>
                </div>
                """
        
        test_html += """
        </body>
        </html>
        """
        
        with open("simple_screenshot_test.html", "w", encoding="utf-8") as f:
            f.write(test_html)
        
        print(f"\n💾 Simple test saved to: simple_screenshot_test.html")
        print("📧 Open this file in a browser to verify screenshots work")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_screenshot_visibility()
