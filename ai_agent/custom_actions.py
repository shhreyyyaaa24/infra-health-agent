"""
Custom action handlers for infrastructure health agent.
Handles cron scheduling and SMTP email sending via configured provider.
"""

import logging
from datetime import datetime

from config import SEND_TIME
from config.constants import DEFAULT_SCHEDULE_DAY
from data.fetcher import fetch_all_environment_data
from data.screenshotter import take_screenshots
from email_module.email_composer import build_html_email
from email_module.mailer import send_email_with_attachments, preview_email_html


class CustomActionHandler:
    """Handles custom actions for email notifications and scheduling."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("CustomActionHandler initialized")
        self.scheduler = None

    def compose_email(self, all_data=None, screenshot_paths=None):
        """Build final HTML email from data (with screenshots optional)"""
        if all_data is None:
            all_data = fetch_all_environment_data()

        if screenshot_paths is None:
            screenshot_paths = take_screenshots()

        return build_html_email(all_data, screenshot_paths), all_data, screenshot_paths

    def send_report_email(self, html_body=None, screenshot_paths=None, all_data=None, dry_run=False):
        """Send an email report using the configured provider."""
        try:
            if html_body is None or all_data is None:
                html_body, all_data, screenshot_paths = self.compose_email(all_data=all_data, screenshot_paths=screenshot_paths)

            self.logger.info("Sending report email (dry_run=%s)...", dry_run)
            result = send_email_with_attachments(html_body, screenshot_paths, dry_run=dry_run, all_data=all_data)

            if result:
                self.logger.info("Report email sent successfully")
            else:
                self.logger.warning("Report email sending failed")

            return result

        except Exception as e:
            self.logger.error("Error in send_report_email: %s", e)
            return False

    def preview_report_email(self, all_data=None, screenshot_paths=None):
        """Preview the email content without sending."""
        if all_data is None or screenshot_paths is None:
            html_body, all_data, screenshot_paths = self.compose_email(all_data=all_data, screenshot_paths=screenshot_paths)

        return preview_email_html(all_data, screenshot_paths)

    def schedule_report_cron(self, day_of_week=DEFAULT_SCHEDULE_DAY, send_time=SEND_TIME, timezone=None):
        """Schedule a weekly cron job for sending the report."""
        try:
            from apscheduler.schedulers.background import BackgroundScheduler
            from apscheduler.triggers.cron import CronTrigger
        except ImportError:
            self.logger.error("APScheduler is required for cron scheduling. Install with: pip install apscheduler")
            raise

        hour, minute = map(int, send_time.split(":"))

        self.scheduler = BackgroundScheduler(timezone=timezone)
        trigger = CronTrigger(day_of_week=day_of_week, hour=hour, minute=minute, timezone=timezone)

        self.scheduler.add_job(
            self.send_report_email,
            trigger=trigger,
            id="weekly_smtp_health_report",
            name="Weekly SMTP Health Report",
            replace_existing=True,
        )

        self.scheduler.start()
        self.logger.info("Scheduled weekly report: %s @ %s", day_of_week, send_time)

        return self.scheduler

    def stop_scheduler(self):
        """Stop the scheduler gracefully."""
        if self.scheduler and self.scheduler.running:
            self.scheduler.shutdown(wait=False)
            self.logger.info("Scheduler stopped")
