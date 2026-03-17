#!/usr/bin/env python3
"""
Setup and test scheduling for automated reports
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_scheduling():
    """Test the scheduling functionality"""
    print("⏰ Testing Scheduling for Automated Reports\n")
    
    try:
        from config.user_config import user_config
        from main import run_scheduler
        
        print("📅 Current Schedule Configuration:")
        print(f"   Send Time: {user_config.SEND_TIME}")
        print(f"   Email Provider: {user_config.EMAIL_PROVIDER}")
        print(f"   Recipient: {user_config.EMAIL_CONFIG[user_config.EMAIL_PROVIDER]['to_emails'][0]}")
        
        print("\n🔄 Starting scheduler...")
        print("   - Scheduler will run every Friday at configured time")
        print("   - Press Ctrl+C to stop the scheduler")
        print("   - Use --dry-run flag to preview without sending")
        
        # Start scheduler
        success = run_scheduler()
        
        return success
        
    except KeyboardInterrupt:
        print("\n⏹️  Scheduler stopped by user")
        return True
    except Exception as e:
        print(f"❌ Scheduler test failed: {e}")
        return False

def show_scheduling_commands():
    """Show available scheduling commands"""
    print("\n📋 Available Scheduling Commands:")
    print("   # Test once with screenshots (dry run)")
    print("   python3 main.py --dry-run")
    print()
    print("   # Run once and send real email")
    print("   python3 main.py")
    print()
    print("   # Start automated scheduler")
    print("   python3 main.py --schedule")
    print()
    print("   # Start scheduler with dry run (for testing)")
    print("   python3 main.py --schedule --dry-run")

if __name__ == "__main__":
    print("Choose your option:")
    print("1. Test scheduling functionality")
    print("2. Show scheduling commands")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        test_scheduling()
    else:
        show_scheduling_commands()
