"""
Main CLI entry point for Infrastructure Health Agent
"""

import argparse
import sys
import os
from datetime import datetime

# Load environment variables first
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not available, will use existing env vars

# Import our modules
from data.fetcher import fetch_all_environment_data, get_summary_stats
from data.screenshotter import take_screenshots, login_and_save_state
from email_module.email_composer import build_html_email
from email_module.mailer import send_email_with_attachments, preview_email_html
from config import SEND_TIME, SCHEDULE_DAY, EMAIL_CRON_SCHEDULE
from config.constants import DEFAULT_SCHEDULE_DAY

# Import AI Agent
try:
    from ai_agent import InfrastructureHealthAgent
    from ai_agent.custom_actions import CustomActionHandler
    AI_AGENT_AVAILABLE = True
except ImportError:
    AI_AGENT_AVAILABLE = False


def run_ai_agent(dry_run=False):
    """Run the AI Agent for intelligent infrastructure monitoring"""
    if not AI_AGENT_AVAILABLE:
        print("❌ AI Agent not available. Please install required dependencies.")
        return False
    
    print("🤖 Starting AI Agent for intelligent infrastructure monitoring...")
    
    # Initialize AI Agent
    agent = InfrastructureHealthAgent(learning_enabled=True)
    
    # Run intelligent monitoring cycle
    cycle_summary = agent.run_intelligent_cycle()
    
    # Display results
    print(f"\n📊 AI Agent Cycle Summary:")
    print(f"   Duration: {cycle_summary['duration_seconds']:.2f} seconds")
    print(f"   Decisions Made: {cycle_summary['decisions_made']}")
    print(f"   Actions Executed: {cycle_summary['actions_executed']}")
    
    # Show AI insights
    if cycle_summary['ai_insights']:
        insights = cycle_summary['ai_insights']
        print(f"\n🧠 AI Insights:")
        print(f"   Anomalies Detected: {len(insights.get('anomalies', []))}")
        print(f"   Trends Identified: {len(insights.get('trends', []))}")
        print(f"   Critical Issues: {len(insights.get('critical_issues', []))}")
        print(f"   Recommendations: {len(insights.get('recommendations', []))}")
        
        if insights.get('predictions'):
            print(f"   Predictions: {len(insights['predictions'])}")
            for pred in insights['predictions'][:3]:  # Show top 3
                print(f"     • {pred['description']} (Confidence: {pred['confidence']}%)")
    
    # Show agent status
    agent_status = agent.get_agent_status()
    print(f"\n📈 AI Agent Status:")
    print(f"   Capabilities: {', '.join(agent_status['capabilities'])}")
    print(f"   Decisions in History: {agent_status['decisions_history_count']}")
    print(f"   Learning Enabled: {agent_status['learning_enabled']}")
    
    return True


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
        success = send_email_with_attachments(html_body, screenshot_paths, all_data=all_data)
        if success:
            print("Process completed successfully!")
        else:
            print("Failed to send email.")
            return False
    
    return True


def run_scheduler():
    """Run the scheduler for periodic execution"""
    try:
        import time
        from ai_agent.custom_actions import CustomActionHandler
    except ImportError:
        print("APScheduler is required for scheduler mode. Install with: pip install apscheduler")
        return False

    # Check if cron scheduling is enabled
    if not EMAIL_CRON_SCHEDULE.get('enabled', True):
        print("Email cron scheduling is disabled in config")
        return False

    # Get schedule configuration
    schedule_day = EMAIL_CRON_SCHEDULE.get('day_of_week', SCHEDULE_DAY)
    send_time = EMAIL_CRON_SCHEDULE.get('send_time', SEND_TIME)
    timezone = EMAIL_CRON_SCHEDULE.get('timezone')

    # Validate send_time format
    try:
        hour, minute = map(int, send_time.split(':'))
    except ValueError:
        print(f"Invalid send_time format: {send_time}. Use HH:MM format.")
        return False

    print(f"Starting scheduler - will run every {schedule_day} at {send_time}")
    if timezone:
        print(f"Timezone: {timezone}")
    print("Press Ctrl+C to stop the scheduler")

    handler = CustomActionHandler()
    handler.schedule_report_cron(day_of_week=schedule_day, send_time=send_time, timezone=timezone)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nScheduler stopped by user")
        handler.stop_scheduler()
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
    
    parser.add_argument(
        '--ai-agent',
        action='store_true',
        help='Run AI Agent for intelligent monitoring and decision-making'
    )
    
    args = parser.parse_args()
    
    print("Infrastructure Health Agent")
    print("=" * 40)
    
    # Handle AI Agent mode
    if args.ai_agent:
        if not AI_AGENT_AVAILABLE:
            print("❌ AI Agent not available. Please install required dependencies:")
            print("   pip install numpy")
            return
        
        success = run_ai_agent(dry_run=args.dry_run)
        if not success:
            sys.exit(1)
        return
    
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
