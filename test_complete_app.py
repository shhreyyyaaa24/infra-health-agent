#!/usr/bin/env python3
"""
Test the complete main application with personalized email
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_complete_app():
    """Test the complete main application flow"""
    print("🚀 Testing Complete Main Application\n")
    
    try:
        # Import main function
        from main import run_once
        
        print("📊 Running complete infrastructure health check...")
        print("   - Fetching data from API")
        print("   - Taking screenshots (with fallback)")
        print("   - Building personalized HTML email")
        print("   - Sending via Gmail")
        
        # Run with real email
        success = run_once(dry_run=False)
        
        if success:
            print("✅ Complete application test successful!")
            print("📬 Check your email for the personalized infrastructure report")
        else:
            print("❌ Application test failed")
        
        return success
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_complete_app()
