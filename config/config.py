"""
Configuration loader for Infrastructure Health Agent
Combines system constants with user configuration
"""

from .constants import *
from .user_config import user_config

# Email Provider Configuration
EMAIL_PROVIDER = user_config.EMAIL_PROVIDER

# Director Configuration Template
DIRECTOR_CONFIG = user_config.DIRECTOR_CONFIG

# API Configuration
API_ENDPOINT = user_config.API_ENDPOINT
USE_WINDOWS_AUTH = user_config.USE_WINDOWS_AUTH
BASIC_AUTH_USER = user_config.BASIC_AUTH_USER
BASIC_AUTH_PASS = user_config.BASIC_AUTH_PASS
COOKIES_FILE = user_config.COOKIES_FILE

# Environment configurations (merge defaults with custom)
ENVIRONMENTS = DEFAULT_ENVIRONMENTS.copy()
if user_config.CUSTOM_ENVIRONMENTS:
    ENVIRONMENTS.update(user_config.CUSTOM_ENVIRONMENTS)

# Screenshot Configuration
SCREENSHOT_HEADLESS = user_config.SCREENSHOT_HEADLESS
SCREENSHOT_DIR = user_config.SCREENSHOT_DIR or DEFAULT_SCREENSHOT_DIR
SCREENSHOT_SELECTOR = user_config.SCREENSHOT_SELECTOR or DEFAULT_SCREENSHOT_SELECTOR

# Dashboard Configuration
DASHBOARD_BASE_URL = user_config.DASHBOARD_BASE_URL
DASHBOARD_TAB_URLS = user_config.DASHBOARD_TAB_URLS

# Email Configuration Template
EMAIL_CONFIG = user_config.EMAIL_CONFIG

# Scheduling
SEND_TIME = user_config.SEND_TIME or DEFAULT_SEND_TIME
SCHEDULE_DAY = user_config.SCHEDULE_DAY or DEFAULT_SCHEDULE_DAY

# Email Cron Schedule Configuration
EMAIL_CRON_SCHEDULE = user_config.EMAIL_CRON_SCHEDULE

# Additional Settings
DEBUG_MODE = user_config.DEBUG_MODE
LOG_LEVEL = user_config.LOG_LEVEL
