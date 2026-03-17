#!/usr/bin/env python3
"""
Debug the data structure to fix the email issue
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def debug_data_structure():
    """Debug the data structure to understand the format"""
    print("🔍 Debugging Data Structure\n")
    
    try:
        from data.fetcher import fetch_all_environment_data
        
        print("📊 Fetching infrastructure data...")
        all_data = fetch_all_environment_data()
        
        if not all_data:
            print("❌ No data fetched")
            return False
        
        print(f"✅ Data fetched: {len(all_data)} environments")
        
        for env_name, projects in all_data.items():
            print(f"\n📁 {env_name.upper()} Environment:")
            print(f"   Number of projects: {len(projects)}")
            
            if projects:
                first_project = projects[0]
                print(f"   First project keys: {list(first_project.keys())}")
                print(f"   First project sample: {first_project}")
        
        return True
        
    except Exception as e:
        print(f"❌ Debug failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    debug_data_structure()
