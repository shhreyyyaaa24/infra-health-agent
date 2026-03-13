"""
Configuration settings for Infrastructure Health Agent
All user-editable settings are in this file
"""

# Email Provider Configuration
EMAIL_PROVIDER = "outlook"  # Options: "outlook", "gmail"

# Director Configuration Template
DIRECTOR_CONFIG = {
    "name": "DIRECTOR NAME",  # Filter projects by this director name
    "email": "director@example.com",  # Director's email for notifications
    "cc_emails": ["manager@example.com"],  # Additional CC emails
}

# API Configuration
API_ENDPOINT = "https://your-api-server.com/api/projects"
USE_WINDOWS_AUTH = True
BASIC_AUTH_USER = ""
BASIC_AUTH_PASS = ""
COOKIES_FILE = ""

# Environment configurations
ENVIRONMENTS = {
    "gcp": {
        "display_name": "Google Cloud Platform",
        "api_key": "gcp"
    },
    "aws": {
        "display_name": "Amazon Web Services", 
        "api_key": "aws"
    },
    "azure": {
        "display_name": "Microsoft Azure",
        "api_key": "azure"
    }
}

# Screenshot Configuration
SCREENSHOT_HEADLESS = True
SCREENSHOT_DIR = "screenshots"
DASHBOARD_BASE_URL = "https://your-dashboard.com"
DASHBOARD_TAB_URLS = {
    "gcp": f"{DASHBOARD_BASE_URL}/gcp-dashboard",
    "aws": f"{DASHBOARD_BASE_URL}/aws-dashboard", 
    "azure": f"{DASHBOARD_BASE_URL}/azure-dashboard"
}
SCREENSHOT_SELECTOR = "body"

# Email Configuration Template
EMAIL_CONFIG = {
    "outlook": {
        "to_emails": ["recipient@example.com"],
        "cc_emails": ["cc@example.com"],
        "subject_template": "Infrastructure Health Report - {date}"
    },
    "gmail": {
        "sender_email": "your-email@gmail.com",
        "app_password": "your-app-password",  # Use App Password for Gmail
        "to_emails": ["recipient@example.com"],
        "cc_emails": ["cc@example.com"],
        "subject_template": "Infrastructure Health Report - {date}"
    }
}

# Scheduling
SEND_TIME = "09:00"  # 24-hour format

# Status labels and colors
STATUS_LABELS = {
    "HEALTHY": "Healthy",
    "MEDIUM": "Medium Risk", 
    "SEVERE": "Severe Risk"
}

STATUS_COLORS = {
    "HEALTHY": "#28a745",  # Green
    "MEDIUM": "#ffc107",   # Yellow/Orange
    "SEVERE": "#dc3545"    # Red
}
