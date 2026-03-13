"""
Main CLI entry point for Infrastructure Health Agent
"""

import argparse
import sys
import os
from datetime import datetime

# Import our modules
from fetcher import fetch_all_environment_data, get_summary_stats
from screenshotter import take_screenshots, login_and_save_state
from email_composer import build_html_email
from mailer import send_email_with_attachments, preview_email_html
from config import SEND_TIME


def run_once(dry_run=False):
    """Run the complete health check and email process once"""
    print("Starting infrastructure health check...")
    
    # Step 1: Fetch data from API
    print("Fetching data from API...")
    all_data = fetch_all_environment_data()
    
    if not all_data:
        print("No data fetched. Exiting.")
        return False
    
    # Get summary statistics
    stats = get_summary_stats(all_data)
    print(f"Found {stats['total_projects']} projects:")
    print(f"  Healthy: {stats['status_counts']['HEALTHY']}")
    print(f"  Medium Risk: {stats['status_counts']['MEDIUM']}")
    print(f"  Severe Risk: {stats['status_counts']['SEVERE']}")
    
    # Step 2: Take screenshots
    print("Taking dashboard screenshots...")
    screenshot_paths = take_screenshots()
    
    if not screenshot_paths:
        print("Warning: No screenshots were captured.")
    
    # Step 3: Build email
    print("Building email...")
    html_body = build_html_email(all_data, screenshot_paths)
    
    # Step 4: Send or preview email
    if dry_run:
        print("Dry run mode: Previewing email...")
        preview_email_html(all_data, screenshot_paths)
        print("Dry run completed. No email sent.")
    else:
        print("Sending email...")
        success = send_email_with_attachments(html_body, screenshot_paths)
        if success:
            print("Process completed successfully!")
        else:
            print("Failed to send email.")
            return False
    
    return True


def run_scheduler():
    """Run the scheduler for periodic execution"""
    try:
        from apscheduler.schedulers.blocking import BlockingScheduler
        from apscheduler.triggers.cron import CronTrigger
    except ImportError:
        print("APScheduler not installed. Install with: pip install apscheduler")
        return False
    
    # Parse send time
    try:
        hour, minute = map(int, SEND_TIME.split(':'))
    except ValueError:
        print(f"Invalid SEND_TIME format: {SEND_TIME}. Use HH:MM format.")
        return False
    
    print(f"Starting scheduler - will run every Friday at {SEND_TIME}")
    print("Press Ctrl+C to stop the scheduler")
    
    scheduler = BlockingScheduler()
    
    # Schedule job for every Friday at specified time
    scheduler.add_job(
        run_once,
        trigger=CronTrigger(day_of_week='fri', hour=hour, minute=minute),
        id='weekly_health_check',
        name='Weekly Infrastructure Health Check'
    )
    
    try:
        scheduler.start()
    except KeyboardInterrupt:
        print("\nScheduler stopped by user")
        return False
    
    return True


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Infrastructure Health Agent - Monitor and report on infrastructure health"
    )
    
    parser.add_argument(
        '--login',
        action='store_true',
        help='Open browser for manual login and save authentication state'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview email without sending (builds email and saves as HTML draft)'
    )
    
    parser.add_argument(
        '--schedule',
        action='store_true',
        help='Run in scheduler mode (executes every Friday at SEND_TIME)'
    )
    
    args = parser.parse_args()
    
    print("Infrastructure Health Agent")
    print("=" * 40)
    
    # Handle login mode
    if args.login:
        print("Login mode selected...")
        login_and_save_state()
        return
    
    # Handle scheduler mode
    if args.schedule:
        run_scheduler()
        return
    
    # Default: run once
    success = run_once(dry_run=args.dry_run)
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
