"""
User configuration template for Infrastructure Health Agent
Users should modify this file with their specific settings
"""

import os

class UserConfig:
    """User configuration object for infrastructure health monitoring"""
    
    def __init__(self):
        # Email Provider Configuration
        self.EMAIL_PROVIDER = "outlook"  # Options: "outlook", "gmail"
        
        # Director Configuration
        self.DIRECTOR_CONFIG = {
            "name": "Shreya Tiwari",  # Filter projects by this director name
            "email": "shhreyyyaa1@gmail.com",  # Director's email for notifications
            "cc_emails": ["manager@example.com"],  # Additional CC emails
        }
        
        # API Configuration
        self.API_ENDPOINT = "https://your-api-server.com/api/projects"
        self.USE_WINDOWS_AUTH = True
        self.BASIC_AUTH_USER = ""
        self.BASIC_AUTH_PASS = ""
        self.COOKIES_FILE = ""
        
        # Dashboard Configuration
        self.DASHBOARD_BASE_URL = "http://127.0.0.1:63645/"
        self.DASHBOARD_TAB_URLS = {
            "gcp": f"{self.DASHBOARD_BASE_URL}/gcp-dashboard",
            "aws": f"{self.DASHBOARD_BASE_URL}/aws-dashboard", 
            "azure": f"{self.DASHBOARD_BASE_URL}/azure-dashboard"
        }
        self.SCREENSHOT_HEADLESS = True
        self.SCREENSHOT_DIR = "screenshots"
        self.SCREENSHOT_SELECTOR = "body"
        
        # Email Configuration Templates
        self.EMAIL_CONFIG = {
            "outlook": {
                "to_emails": ["recipient@example.com"],
                "cc_emails": ["cc@example.com"],
                "subject_template": "Infrastructure Health Report - {date}"
            },
            "gmail": {
                "sender_email": "shreyaa.developer@gmail.com",
                "app_password": os.getenv("GMAIL_APP_PASSWORD"),
                "to_emails": ["shhreyyyaa1@gmail.com"],
                "cc_emails": [""],
                "subject_template": "Infrastructure Health Report - {date}"
            }
        }
        
        # Scheduling Configuration
        self.SEND_TIME = "09:00"  # 24-hour format
        
        # Environment Customization (optional - override defaults if needed)
        self.CUSTOM_ENVIRONMENTS = {
            # Add custom environment configurations here
            # Example:
            # "custom_env": {
            #     "display_name": "Custom Environment",
            #     "api_key": "custom"
            # }
        }
        
        # Additional Settings
        self.DEBUG_MODE = False
        self.LOG_LEVEL = "INFO"  # Options: "DEBUG", "INFO", "WARNING", "ERROR"

# Create global configuration instance
user_config = UserConfig()
