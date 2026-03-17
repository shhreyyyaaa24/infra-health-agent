#!/usr/bin/env python3
"""
Test the main application with screenshots and email
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_with_screenshots():
    """Test main application with screenshots and email"""
    print("🚀 Testing Main Application with Screenshots\n")
    
    try:
        # Import main function
        from main import run_once
        
        print("📸 Running complete infrastructure health check...")
        print("   - Fetching data from API")
        print("   - Taking screenshots")
        print("   - Building HTML email")
        print("   - Sending via Gmail")
        
        # Run with dry-run first to preview
        print("\n🔍 First: Dry run (preview only)...")
        success = run_once(dry_run=True)
        
        if not success:
            print("❌ Dry run failed")
            return False
        
        print("\n📧 Now: Send real email with screenshots...")
        success = run_once(dry_run=False)
        
        if success:
            print("✅ Complete test successful!")
            print("📬 Check your email for the full infrastructure report with screenshots")
        else:
            print("❌ Real email send failed")
        
        return success
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    test_with_screenshots()
