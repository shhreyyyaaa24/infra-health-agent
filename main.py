"""
Infrastructure Health Agent - Main Entry Point

A simple, clean CLI tool for monitoring infrastructure health with AI-powered analysis.
"""

import sys
import argparse
from typing import Optional

# Load environment variables first
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not available, will use existing env vars

# Core imports
from data.fetcher import fetch_all_environment_data, get_summary_stats
from data.screenshotter import take_screenshots
from email_module.email_composer import build_html_email
from email_module.mailer import send_email_with_attachments, preview_email_html
from config import EMAIL_CRON_SCHEDULE

# AI Agent (optional dependency)
try:
    from ai_agent import InfrastructureHealthAgent
    from ai_agent.custom_actions import CustomActionHandler
    AI_AGENT_AVAILABLE = True
except ImportError:
    AI_AGENT_AVAILABLE = False


class InfrastructureHealthMonitor:
    """Main class for infrastructure health monitoring"""
    
    def __init__(self):
        self.ai_agent: Optional[InfrastructureHealthAgent] = None
        
    def run_health_check(self, dry_run: bool = False) -> bool:
        """Run complete health check and send report"""
        print("Starting infrastructure health check...")
        
        # Step 1: Fetch infrastructure data
        data = self._fetch_data()
        if not data:
            return False
            
        # Step 2: Capture dashboard screenshots
        screenshots = self._capture_screenshots()
        
        # Step 3: Generate and send report
        return self._send_report(data, screenshots, dry_run)
    
    def _fetch_data(self):
        """Fetch data from infrastructure APIs"""
        print("Fetching infrastructure data...")
        
        all_data = fetch_all_environment_data()
        if not all_data:
            print("No data fetched. Please check API configuration.")
            return None
            
        # Show summary
        stats = get_summary_stats(all_data)
        print(f"Found {stats['total_projects']} projects:")
        print(f"   Healthy: {stats['status_counts']['HEALTHY']}")
        print(f"   Medium Risk: {stats['status_counts']['MEDIUM']}")
        print(f"   Severe Risk: {stats['status_counts']['SEVERE']}")
        
        return all_data
    
    def _capture_screenshots(self):
        """Capture dashboard screenshots"""
        print("Capturing dashboard screenshots...")
        
        screenshots = take_screenshots()
        if not screenshots:
            print("Warning: No screenshots captured. Check dashboard URLs.")
            
        return screenshots
    
    def _send_report(self, data, screenshots, dry_run: bool) -> bool:
        """Generate and send email report"""
        print("Generating report...")
        
        html_content = build_html_email(data, screenshots)
        
        if dry_run:
            print("Dry run: Previewing email...")
            preview_email_html(data, screenshots)
            print("Dry run completed successfully!")
            return True
        else:
            print("Sending email report...")
            success = send_email_with_attachments(html_content, screenshots, all_data=data)
            
            if success:
                print("Report sent successfully!")
                return True
            else:
                print("Failed to send report.")
                return False
    
    def run_ai_monitoring(self, dry_run: bool = False) -> bool:
        """Run AI-powered intelligent monitoring"""
        if not AI_AGENT_AVAILABLE:
            print("AI Agent not available. Install with: pip install numpy scipy")
            return False
            
        print("Starting AI-powered monitoring...")
        
        # Initialize AI agent
        agent = InfrastructureHealthAgent(learning_enabled=True)
        
        # Run intelligent monitoring cycle
        results = agent.run_intelligent_cycle()
        
        # Display results
        self._display_ai_results(results)
        
        return True
    
    def _display_ai_results(self, results):
        """Display AI monitoring results in a clean format"""
        print("\nAI Monitoring Results:")
        print(f"   Duration: {results['duration_seconds']:.2f}s")
        print(f"   Decisions: {results['decisions_made']}")
        print(f"   Actions: {results['actions_executed']}")
        
        insights = results.get('ai_insights', {})
        if insights:
            print("\nAI Insights:")
            print(f"   Anomalies: {len(insights.get('anomalies', []))}")
            print(f"   Trends: {len(insights.get('trends', []))}")
            print(f"   Critical Issues: {len(insights.get('critical_issues', []))}")
            print(f"   Recommendations: {len(insights.get('recommendations', []))}")
            
            # Show top predictions
            predictions = insights.get('predictions', [])[:3]
            if predictions:
                print("   Top Predictions:")
                for pred in predictions:
                    print(f"      • {pred['description']} ({pred['confidence']}% confidence)")
    
    def run_scheduler(self) -> bool:
        """Start the automated scheduler"""
        if not AI_AGENT_AVAILABLE:
            print("Scheduler requires AI Agent. Install with: pip install apscheduler")
            return False
            
        if not EMAIL_CRON_SCHEDULE.get('enabled', True):
            print("Scheduler disabled in configuration")
            return False
        
        # Get schedule settings
        schedule_config = {
            'day': EMAIL_CRON_SCHEDULE.get('day_of_week', 'fri'),
            'time': EMAIL_CRON_SCHEDULE.get('send_time', '09:00'),
            'timezone': EMAIL_CRON_SCHEDULE.get('timezone')
        }
        
        # Validate time format
        try:
            hour, minute = map(int, schedule_config['time'].split(':'))
        except ValueError:
            print(f"Invalid time format: {schedule_config['time']}. Use HH:MM")
            return False
        
        print(f"Starting scheduler...")
        print(f"   Schedule: Every {schedule_config['day']} at {schedule_config['time']}")
        if schedule_config['timezone']:
            print(f"   Timezone: {schedule_config['timezone']}")
        print("   Press Ctrl+C to stop")
        
        # Start scheduler
        handler = CustomActionHandler()
        handler.schedule_report_cron(
            day_of_week=schedule_config['day'],
            send_time=schedule_config['time'],
            timezone=schedule_config['timezone']
        )
        
        # Keep running until interrupted
        try:
            import time
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nScheduler stopped by user")
            handler.stop_scheduler()
            
        return True


def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser"""
    parser = argparse.ArgumentParser(
        description="Infrastructure Health Agent - AI-powered infrastructure monitoring",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Run health check once
  %(prog)s --dry-run         # Preview report without sending
  %(prog)s --ai-agent        # Run AI-powered monitoring
  %(prog)s --schedule        # Start automated scheduler
        """
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview report without sending email'
    )
    
    parser.add_argument(
        '--ai-agent',
        action='store_true',
        help='Run AI-powered intelligent monitoring'
    )
    
    parser.add_argument(
        '--schedule',
        action='store_true',
        help='Start automated scheduler'
    )
    
    return parser


def main():
    """Main entry point"""
    parser = create_parser()
    args = parser.parse_args()
    
    # Show welcome message
    print("Infrastructure Health Agent")
    print("=" * 40)
    
    # Initialize monitor
    monitor = InfrastructureHealthMonitor()
    
    # Route to appropriate mode
    if args.ai_agent:
        success = monitor.run_ai_monitoring(dry_run=args.dry_run)
        sys.exit(0 if success else 1)
        
    elif args.schedule:
        success = monitor.run_scheduler()
        sys.exit(0 if success else 1)
        
    else:
        # Default: run health check once
        success = monitor.run_health_check(dry_run=args.dry_run)
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
