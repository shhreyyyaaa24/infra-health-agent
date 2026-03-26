"""
User configuration template for Infrastructure Health Agent
Users should modify this file with their specific settings
"""

import os

class UserConfig:
    """User configuration object for infrastructure health monitoring"""
    
    def __init__(self):
        # Email Provider Configuration
        self.EMAIL_PROVIDER = "gmail"  # Options: "outlook", "gmail"
        
        # Director Configuration
        self.DIRECTOR_CONFIG = {
            "name": "Shreya Tiwari",  # Filter projects by this director name
            "email": "shhreyyyaa1@gmail.com",  # Director's email for notifications
            "cc_emails": [""],  # Additional CC emails
        }
        
        # API Configuration
        self.API_ENDPOINT = "https://your-api-server.com/api/projects"
        
        # Custom Environments (optional - override/add to default environments)
        self.CUSTOM_ENVIRONMENTS = {}  # Example: {"custom_env": {"display_name": "Custom", "api_key": "custom"}}
        
        # Dashboard Configuration
        self.DASHBOARD_BASE_URL = "http://localhost:5173"
        self.DASHBOARD_TAB_URLS = {
            "gcp": f"{self.DASHBOARD_BASE_URL}/gcp-dashboard",
            "aws": f"{self.DASHBOARD_BASE_URL}/aws-dashboard", 
            "azure": f"{self.DASHBOARD_BASE_URL}/azure-dashboard"
        }
        self.SCREENSHOT_HEADLESS = True
        self.SCREENSHOT_DIR = "screenshots"
        self.SCREENSHOT_SELECTOR = ".cloud-card"  # Target specific component cards
        
        # Email Configuration Templates - only sensitive data from env var
        self.EMAIL_CONFIG = {
            "outlook": {
                "sender_email": "your-outlook@outlook.com",
                "app_password": os.getenv("OUTLOOK_APP_PASSWORD", ""),  # Get from environment variable
                "to_emails": ["shhreyyyaa1@gmail.com"],
                "cc_emails": [""],
                "subject_template": "Infrastructure Health Report - {date}"
            },
            "gmail": {
                "sender_email": "shreyaa.developer@gmail.com",
                "app_password": os.getenv("GMAIL_APP_PASSWORD", ""),  # Get from environment variable
                "to_emails": ["shhreyyyaa1@gmail.com"],
                "cc_emails": [""],
                "subject_template": "Infrastructure Health Report - {date}"
            }
        }
        
        # Scheduling Configuration
        self.SEND_TIME = "09:00"  # 24-hour format (HH:MM)
        self.SCHEDULE_DAY = "fri"  # Day of week: "mon", "tue", "wed", "thu", "fri", "sat", "sun"
        
        # Email Cron Schedule Configuration
        self.EMAIL_CRON_SCHEDULE = {
            "enabled": True,  # Enable/disable cron-based email scheduling
            "day_of_week": self.SCHEDULE_DAY,  # Day of week for cron schedule
            "send_time": self.SEND_TIME,  # Time to send (HH:MM in 24-hour format)
            "timezone": None,  # Optional timezone (e.g., "US/Eastern", "UTC"). None = system default
        }
        
        # Additional Settings
        self.DEBUG_MODE = False
        self.LOG_LEVEL = "INFO"  # Options: "DEBUG", "INFO", "WARNING", "ERROR"

# Create global configuration instance
user_config = UserConfig()
