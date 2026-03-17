#!/usr/bin/env python3
"""
Test dashboard connectivity and screenshot capture
"""

import os
import sys
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_dashboard_connectivity():
    """Test if the dashboard is accessible"""
    print("🌐 Testing Dashboard Connectivity\n")
    
    # Import config to get current dashboard URL
    from config.user_config import user_config
    base_url = user_config.DASHBOARD_BASE_URL
    dashboard_urls = user_config.DASHBOARD_TAB_URLS
    
    print(f"🔍 Testing base URL: {base_url}")
    
    # Test base URL
    try:
        response = requests.get(base_url, timeout=5)
        print(f"✅ Base URL accessible: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print(f"❌ Base URL not accessible - Dashboard server not running")
        print(f"💡 Please start your dashboard server at {base_url}")
        return False
    except requests.exceptions.Timeout:
        print(f"❌ Base URL timeout - Server may be slow")
        return False
    except Exception as e:
        print(f"❌ Base URL error: {e}")
        return False
    
    # Test dashboard URLs
    print(f"\n🔍 Testing dashboard URLs:")
    for env, url in dashboard_urls.items():
        try:
            response = requests.get(url, timeout=5)
            print(f"   ✅ {env.upper()}: {url} ({response.status_code})")
        except requests.exceptions.ConnectionError:
            print(f"   ❌ {env.upper()}: {url} - Connection refused")
        except requests.exceptions.Timeout:
            print(f"   ⏰ {env.upper()}: {url} - Timeout")
        except Exception as e:
            print(f"   ❌ {env.upper()}: {url} - {e}")
    
    return True

def test_screenshot_capture():
    """Test screenshot capture with current dashboard"""
    print("\n📸 Testing Screenshot Capture\n")
    
    try:
        from data.screenshotter import take_screenshots
        
        print("🔄 Attempting to capture screenshots...")
        screenshot_paths = take_screenshots()
        
        if screenshot_paths:
            print(f"✅ Screenshots captured successfully:")
            for path in screenshot_paths:
                print(f"   📎 {path}")
            return True
        else:
            print("❌ No screenshots captured")
            return False
            
    except Exception as e:
        print(f"❌ Screenshot capture failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Dashboard Screenshot Test\n")
    
    # Test connectivity first
    connectivity_ok = test_dashboard_connectivity()
    
    if connectivity_ok:
        # Test screenshot capture
        screenshot_ok = test_screenshot_capture()
        
        if screenshot_ok:
            print("\n🎉 Success! Dashboard screenshots are working!")
            print("📧 You can now run: python3 main.py")
        else:
            print("\n⚠️ Dashboard is accessible but screenshots failed")
            print("💡 Check if Playwright browsers are installed")
    else:
        print("\n❌ Dashboard server is not running")
        print("💡 Please start your dashboard server first")
