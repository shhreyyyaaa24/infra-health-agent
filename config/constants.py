"""
System constants for Infrastructure Health Agent
These values should not be modified by users
"""

# Default environment configurations
DEFAULT_ENVIRONMENTS = {
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

# Screenshot defaults
DEFAULT_SCREENSHOT_DIR = "screenshots"
DEFAULT_SCREENSHOT_SELECTOR = "body"

# Email provider options
EMAIL_PROVIDERS = {
    "outlook": "Outlook (Windows COM interface)",
    "gmail": "Gmail (SMTP with App Password)"
}

# Default scheduling
DEFAULT_SEND_TIME = "09:00"  # 24-hour format
DEFAULT_SCHEDULE_DAY = "fri"  # Friday

# File paths
AUTH_STATE_FILE = "auth_state.json"
DRAFT_EMAIL_FILE = "draft_email"
PREVIEW_EMAIL_FILE = "email_preview.html"

# API defaults
DEFAULT_API_TIMEOUT = 30
DEFAULT_LOGIN_WAIT_TIME = 30  # seconds

# Status computation thresholds
DEFAULT_CPU_BUDGET_PERCENT = 100
DEFAULT_SHUTDOWN_THRESHOLD_RATIO = 0.9
