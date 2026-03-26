"""
Test cases for email module functionality
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import smtplib

# Add the parent directory to the path to import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from email_module.email_composer import build_html_email
from email_module.mailer import send_email_with_attachments, preview_email_html


class TestEmailComposer(unittest.TestCase):
    """Test cases for email composition functionality"""
    
    def test_build_html_email_basic(self):
        """Test basic HTML email generation"""
        test_data = [
            {'name': 'project1', 'status': 'HEALTHY', 'environment': 'prod'},
            {'name': 'project2', 'status': 'MEDIUM', 'environment': 'dev'}
        ]
        test_screenshots = ['screenshot1.png', 'screenshot2.png']
        
        html_content = build_html_email(test_data, test_screenshots)
        
        self.assertIsInstance(html_content, str)
        self.assertIn('<html>', html_content)
        self.assertIn('project1', html_content)
        self.assertIn('project2', html_content)
        self.assertIn('HEALTHY', html_content)
        self.assertIn('MEDIUM', html_content)
    
    def test_build_html_email_empty_data(self):
        """Test HTML email generation with empty data"""
        test_data = []
        test_screenshots = []
        
        html_content = build_html_email(test_data, test_screenshots)
        
        self.assertIsInstance(html_content, str)
        self.assertIn('<html>', html_content)
    
    def test_build_html_email_no_screenshots(self):
        """Test HTML email generation without screenshots"""
        test_data = [
            {'name': 'project1', 'status': 'HEALTHY', 'environment': 'prod'}
        ]
        test_screenshots = []
        
        html_content = build_html_email(test_data, test_screenshots)
        
        self.assertIsInstance(html_content, str)
        self.assertIn('project1', html_content)
    
    def test_build_html_email_severe_issues(self):
        """Test HTML email generation with severe issues"""
        test_data = [
            {'name': 'project1', 'status': 'SEVERE', 'environment': 'prod'},
            {'name': 'project2', 'status': 'HEALTHY', 'environment': 'dev'}
        ]
        test_screenshots = ['screenshot.png']
        
        html_content = build_html_email(test_data, test_screenshots)
        
        self.assertIsInstance(html_content, str)
        self.assertIn('SEVERE', html_content)
        # Should contain alert styling for severe issues
        self.assertTrue('alert' in html_content.lower() or 'critical' in html_content.lower())


class TestEmailMailer(unittest.TestCase):
    """Test cases for email sending functionality"""
    
    @patch('email_module.mailer.smtplib.SMTP')
    @patch('email_module.mailer.user_config')
    def test_send_email_gmail_success(self, mock_config, mock_smtp):
        """Test successful Gmail email sending"""
        # Mock configuration
        mock_config.EMAIL_PROVIDER = "gmail"
        mock_config.EMAIL_CONFIG = {
            'gmail': {
                'sender_email': 'test@gmail.com',
                'app_password': 'app_password',
                'to_emails': ['recipient@example.com'],
                'cc_emails': [],
                'subject_template': 'Infrastructure Report - {date}'
            }
        }
        
        # Mock SMTP server
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        test_html = '<html>Test Report</html>'
        test_screenshots = ['screenshot.png']
        test_data = [{'name': 'project1', 'status': 'HEALTHY'}]
        
        result = send_email_with_attachments(test_html, test_screenshots, all_data=test_data)
        
        self.assertTrue(result)
        mock_smtp.assert_called_with('smtp.gmail.com', 587)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once()
        mock_server.send_message.assert_called_once()
    
    @patch('email_module.mailer.smtplib.SMTP')
    @patch('email_module.mailer.user_config')
    def test_send_email_outlook_success(self, mock_config, mock_smtp):
        """Test successful Outlook email sending"""
        # Mock configuration
        mock_config.EMAIL_PROVIDER = "outlook"
        mock_config.EMAIL_CONFIG = {
            'outlook': {
                'sender_email': 'test@outlook.com',
                'app_password': 'app_password',
                'to_emails': ['recipient@example.com'],
                'cc_emails': [],
                'subject_template': 'Infrastructure Report - {date}'
            }
        }
        
        # Mock SMTP server
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        test_html = '<html>Test Report</html>'
        test_screenshots = []
        test_data = []
        
        result = send_email_with_attachments(test_html, test_screenshots, all_data=test_data)
        
        self.assertTrue(result)
        mock_smtp.assert_called_with('smtp-mail.outlook.com', 587)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once()
    
    @patch('email_module.mailer.smtplib.SMTP')
    @patch('email_module.mailer.user_config')
    def test_send_email_smtp_error(self, mock_config, mock_smtp):
        """Test email sending with SMTP error"""
        # Mock configuration
        mock_config.EMAIL_PROVIDER = "gmail"
        mock_config.EMAIL_CONFIG = {
            'gmail': {
                'sender_email': 'test@gmail.com',
                'app_password': 'app_password',
                'to_emails': ['recipient@example.com'],
                'cc_emails': [],
                'subject_template': 'Infrastructure Report - {date}'
            }
        }
        
        # Mock SMTP error
        mock_smtp.side_effect = smtplib.SMTPException("SMTP Error")
        
        test_html = '<html>Test Report</html>'
        test_screenshots = []
        test_data = []
        
        result = send_email_with_attachments(test_html, test_screenshots, all_data=test_data)
        
        self.assertFalse(result)
    
    @patch('builtins.open', create=True)
    @patch('email_module.mailer.user_config')
    def test_send_email_attachment_error(self, mock_config, mock_open):
        """Test email sending with attachment error"""
        # Mock configuration
        mock_config.EMAIL_PROVIDER = "gmail"
        mock_config.EMAIL_CONFIG = {
            'gmail': {
                'sender_email': 'test@gmail.com',
                'app_password': 'app_password',
                'to_emails': ['recipient@example.com'],
                'cc_emails': [],
                'subject_template': 'Infrastructure Report - {date}'
            }
        }
        
        # Mock file open error
        mock_open.side_effect = FileNotFoundError("File not found")
        
        test_html = '<html>Test Report</html>'
        test_screenshots = ['nonexistent.png']
        test_data = []
        
        result = send_email_with_attachments(test_html, test_screenshots, all_data=test_data)
        
        # Should still send email even if attachment fails
        self.assertTrue(result)
    
    @patch('builtins.open', create=True)
    @patch('email_module.mailer.user_config')
    def test_preview_email_html(self, mock_config, mock_open):
        """Test email preview functionality"""
        # Mock configuration
        mock_config.EMAIL_CONFIG = {
            'gmail': {
                'subject_template': 'Infrastructure Report - {date}'
            }
        }
        
        # Mock file operations
        mock_file = MagicMock()
        mock_file.__enter__.return_value = mock_file
        mock_open.return_value = mock_file
        
        test_data = [{'name': 'project1', 'status': 'HEALTHY'}]
        test_screenshots = ['screenshot.png']
        
        preview_email_html(test_data, test_screenshots)
        
        # Verify file was written
        mock_open.assert_called_once()
        mock_file.write.assert_called_once()


if __name__ == '__main__':
    unittest.main()
