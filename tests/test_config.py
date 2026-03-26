"""
Test cases for configuration module functionality
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the parent directory to the path to import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import config, user_config, constants


class TestUserConfig(unittest.TestCase):
    """Test cases for user configuration"""
    
    def test_user_config_initialization(self):
        """Test user configuration initialization"""
        from config.user_config import UserConfig
        
        config_instance = UserConfig()
        
        # Test default values
        self.assertEqual(config_instance.EMAIL_PROVIDER, "gmail")
        self.assertIsInstance(config_instance.DIRECTOR_CONFIG, dict)
        self.assertIn('name', config_instance.DIRECTOR_CONFIG)
        self.assertIn('email', config_instance.DIRECTOR_CONFIG)
        self.assertEqual(config_instance.SEND_TIME, "09:00")
        self.assertEqual(config_instance.SCHEDULE_DAY, "fri")
    
    def test_user_config_email_config(self):
        """Test email configuration structure"""
        from config.user_config import UserConfig
        
        config_instance = UserConfig()
        
        # Test email config structure
        self.assertIn('gmail', config_instance.EMAIL_CONFIG)
        self.assertIn('outlook', config_instance.EMAIL_CONFIG)
        
        gmail_config = config_instance.EMAIL_CONFIG['gmail']
        self.assertIn('sender_email', gmail_config)
        self.assertIn('app_password', gmail_config)
        self.assertIn('to_emails', gmail_config)
        self.assertIn('subject_template', gmail_config)
    
    def test_user_config_dashboard_urls(self):
        """Test dashboard URLs configuration"""
        from config.user_config import UserConfig
        
        config_instance = UserConfig()
        
        # Test dashboard URLs
        self.assertIsInstance(config_instance.DASHBOARD_TAB_URLS, dict)
        self.assertIn('gcp', config_instance.DASHBOARD_TAB_URLS)
        self.assertIn('aws', config_instance.DASHBOARD_TAB_URLS)
        self.assertIn('azure', config_instance.DASHBOARD_TAB_URLS)
        
        # Test URL format
        for name, url in config_instance.DASHBOARD_TAB_URLS.items():
            self.assertTrue(url.startswith('http'))
            self.assertIn(name, url)
    
    def test_user_config_cron_schedule(self):
        """Test cron schedule configuration"""
        from config.user_config import UserConfig
        
        config_instance = UserConfig()
        
        # Test cron schedule structure
        self.assertIsInstance(config_instance.EMAIL_CRON_SCHEDULE, dict)
        self.assertIn('enabled', config_instance.EMAIL_CRON_SCHEDULE)
        self.assertIn('day_of_week', config_instance.EMAIL_CRON_SCHEDULE)
        self.assertIn('send_time', config_instance.EMAIL_CRON_SCHEDULE)
        self.assertIn('timezone', config_instance.EMAIL_CRON_SCHEDULE)
        
        # Test default values
        self.assertTrue(config_instance.EMAIL_CRON_SCHEDULE['enabled'])
        self.assertEqual(config_instance.EMAIL_CRON_SCHEDULE['day_of_week'], 'fri')
        self.assertEqual(config_instance.EMAIL_CRON_SCHEDULE['send_time'], '09:00')
    
    def test_user_config_global_instance(self):
        """Test global user configuration instance"""
        from config.user_config import user_config
        
        self.assertIsNotNone(user_config)
        self.assertIsInstance(user_config, user_config.UserConfig)


class TestConstants(unittest.TestCase):
    """Test cases for system constants"""
    
    def test_constants_import(self):
        """Test constants can be imported"""
        from config.constants import (
            DEFAULT_SCHEDULE_DAY,
            DEFAULT_SEND_TIME,
            SUPPORTED_EMAIL_PROVIDERS,
            HEALTH_STATUS_COLORS,
            EMAIL_TEMPLATES
        )
        
        # Test constants exist and have expected types
        self.assertIsInstance(DEFAULT_SCHEDULE_DAY, str)
        self.assertIsInstance(DEFAULT_SEND_TIME, str)
        self.assertIsInstance(SUPPORTED_EMAIL_PROVIDERS, list)
        self.assertIsInstance(HEALTH_STATUS_COLORS, dict)
        self.assertIsInstance(EMAIL_TEMPLATES, dict)
    
    def test_health_status_colors(self):
        """Test health status color configuration"""
        from config.constants import HEALTH_STATUS_COLORS
        
        # Test required status colors
        self.assertIn('HEALTHY', HEALTH_STATUS_COLORS)
        self.assertIn('MEDIUM', HEALTH_STATUS_COLORS)
        self.assertIn('SEVERE', HEALTH_STATUS_COLORS)
        
        # Test color format (hex codes)
        for status, color in HEALTH_STATUS_COLORS.items():
            self.assertTrue(color.startswith('#'))
            self.assertEqual(len(color), 7)  # #RRGGBB format
    
    def test_email_providers(self):
        """Test supported email providers"""
        from config.constants import SUPPORTED_EMAIL_PROVIDERS
        
        # Test required providers
        self.assertIn('gmail', SUPPORTED_EMAIL_PROVIDERS)
        self.assertIn('outlook', SUPPORTED_EMAIL_PROVIDERS)
    
    def test_email_templates(self):
        """Test email template configuration"""
        from config.constants import EMAIL_TEMPLATES
        
        # Test template structure
        self.assertIn('subject', EMAIL_TEMPLATES)
        self.assertIn('body_header', EMAIL_TEMPLATES)
        self.assertIn('body_footer', EMAIL_TEMPLATES)
        
        # Test templates contain placeholders
        self.assertIn('{date}', EMAIL_TEMPLATES['subject'])


class TestConfigLoader(unittest.TestCase):
    """Test cases for configuration loader"""
    
    def test_config_imports(self):
        """Test configuration module imports"""
        from config import (
            SEND_TIME,
            SCHEDULE_DAY,
            EMAIL_CRON_SCHEDULE,
            API_ENDPOINT,
            EMAIL_PROVIDER
        )
        
        # Test configuration values are accessible
        self.assertIsInstance(SEND_TIME, str)
        self.assertIsInstance(SCHEDULE_DAY, str)
        self.assertIsInstance(EMAIL_CRON_SCHEDULE, dict)
        self.assertIsInstance(API_ENDPOINT, str)
        self.assertIsInstance(EMAIL_PROVIDER, str)
    
    @patch('config.user_config.user_config')
    def test_config_values_from_user_config(self, mock_user_config):
        """Test configuration values come from user config"""
        # Mock user config values
        mock_user_config.SEND_TIME = '10:00'
        mock_user_config.SCHEDULE_DAY = 'mon'
        mock_user_config.EMAIL_CRON_SCHEDULE = {'enabled': True}
        mock_user_config.API_ENDPOINT = 'https://test-api.com'
        mock_user_config.EMAIL_PROVIDER = 'outlook'
        
        # Re-import config to test loading
        import importlib
        import config
        importlib.reload(config)
        
        # Test values are loaded from user config
        self.assertEqual(config.SEND_TIME, '10:00')
        self.assertEqual(config.SCHEDULE_DAY, 'mon')
        self.assertEqual(config.EMAIL_PROVIDER, 'outlook')


class TestEnvironmentVariables(unittest.TestCase):
    """Test cases for environment variable handling"""
    
    @patch.dict(os.environ, {'GMAIL_APP_PASSWORD': 'test_password'})
    def test_gmail_password_env_var(self):
        """Test Gmail password from environment variable"""
        from config.user_config import UserConfig
        
        config_instance = UserConfig()
        
        # Test that environment variable is used
        gmail_config = config_instance.EMAIL_CONFIG['gmail']
        self.assertEqual(gmail_config['app_password'], 'test_password')
    
    @patch.dict(os.environ, {'OUTLOOK_APP_PASSWORD': 'test_password'})
    def test_outlook_password_env_var(self):
        """Test Outlook password from environment variable"""
        from config.user_config import UserConfig
        
        config_instance = UserConfig()
        
        # Test that environment variable is used
        outlook_config = config_instance.EMAIL_CONFIG['outlook']
        self.assertEqual(outlook_config['app_password'], 'test_password')
    
    def test_missing_env_vars(self):
        """Test missing environment variables"""
        from config.user_config import UserConfig
        
        # Clear environment variables
        with patch.dict(os.environ, {}, clear=True):
            config_instance = UserConfig()
            
            # Test that empty string is used as default
            gmail_config = config_instance.EMAIL_CONFIG['gmail']
            outlook_config = config_instance.EMAIL_CONFIG['outlook']
            self.assertEqual(gmail_config['app_password'], '')
            self.assertEqual(outlook_config['app_password'], '')


class TestConfigValidation(unittest.TestCase):
    """Test cases for configuration validation"""
    
    def test_time_format_validation(self):
        """Test time format validation"""
        from config.user_config import UserConfig
        
        config_instance = UserConfig()
        
        # Test valid time format
        valid_time = "09:30"
        try:
            hour, minute = map(int, valid_time.split(':'))
            self.assertEqual(hour, 9)
            self.assertEqual(minute, 30)
        except ValueError:
            self.fail("Valid time format raised ValueError")
        
        # Test invalid time format
        invalid_time = "9:30"
        with self.assertRaises(ValueError):
            hour, minute = map(int, invalid_time.split(':'))
    
    def test_day_of_week_validation(self):
        """Test day of week validation"""
        from config.user_config import UserConfig
        
        config_instance = UserConfig()
        
        # Test valid days
        valid_days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        for day in valid_days:
            self.assertIn(day, valid_days)
        
        # Test schedule day is valid
        self.assertIn(config_instance.SCHEDULE_DAY, valid_days)
        self.assertIn(config_instance.EMAIL_CRON_SCHEDULE['day_of_week'], valid_days)
    
    def test_email_provider_validation(self):
        """Test email provider validation"""
        from config.user_config import UserConfig
        from config.constants import SUPPORTED_EMAIL_PROVIDERS
        
        config_instance = UserConfig()
        
        # Test email provider is supported
        self.assertIn(config_instance.EMAIL_PROVIDER, SUPPORTED_EMAIL_PROVIDERS)


if __name__ == '__main__':
    unittest.main()
