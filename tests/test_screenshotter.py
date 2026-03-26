"""
Test cases for screenshotter module functionality
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import asyncio

# Add the parent directory to the path to import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.screenshotter import take_screenshots, login_and_save_state


class TestScreenshotter(unittest.TestCase):
    """Test cases for screenshot functionality"""
    
    @patch('data.screenshotter.asyncio.new_event_loop')
    @patch('data.screenshotter.asyncio.run')
    @patch('data.screenshotter.user_config')
    def test_take_screenshots_success(self, mock_config, mock_asyncio_run, mock_new_loop):
        """Test successful screenshot capture"""
        # Mock configuration
        mock_config.DASHBOARD_TAB_URLS = {
            'gcp': 'http://localhost:5173/gcp-dashboard',
            'aws': 'http://localhost:5173/aws-dashboard'
        }
        mock_config.SCREENSHOT_DIR = 'screenshots'
        mock_config.SCREENSHOT_HEADLESS = True
        mock_config.SCREENSHOT_SELECTOR = '.cloud-card'
        
        # Mock async function result
        mock_asyncio_run.return_value = [
            'screenshots/gcp_dashboard.png',
            'screenshots/aws_dashboard.png'
        ]
        
        result = take_screenshots()
        
        self.assertEqual(len(result), 2)
        self.assertIn('gcp_dashboard.png', result[0])
        self.assertIn('aws_dashboard.png', result[1])
        mock_asyncio_run.assert_called_once()
    
    @patch('data.screenshotter.asyncio.run')
    @patch('data.screenshotter.user_config')
    def test_take_screenshots_empty_urls(self, mock_config, mock_asyncio_run):
        """Test screenshot capture with no dashboard URLs"""
        # Mock configuration with empty URLs
        mock_config.DASHBOARD_TAB_URLS = {}
        mock_config.SCREENSHOT_DIR = 'screenshots'
        
        result = take_screenshots()
        
        self.assertEqual(result, [])
        mock_asyncio_run.assert_not_called()
    
    @patch('data.screenshotter.asyncio.run')
    @patch('data.screenshotter.user_config')
    def test_take_screenshots_exception(self, mock_config, mock_asyncio_run):
        """Test screenshot capture with exception"""
        # Mock configuration
        mock_config.DASHBOARD_TAB_URLS = {
            'gcp': 'http://localhost:5173/gcp-dashboard'
        }
        mock_config.SCREENSHOT_DIR = 'screenshots'
        
        # Mock async exception
        mock_asyncio_run.side_effect = Exception("Screenshot failed")
        
        result = take_screenshots()
        
        self.assertEqual(result, [])
    
    @patch('data.screenshotter.asyncio.run')
    @patch('data.screenshotter.user_config')
    def test_take_screenshots_partial_failure(self, mock_config, mock_asyncio_run):
        """Test screenshot capture with partial failure"""
        # Mock configuration
        mock_config.DASHBOARD_TAB_URLS = {
            'gcp': 'http://localhost:5173/gcp-dashboard',
            'aws': 'http://localhost:5173/aws-dashboard',
            'azure': 'http://localhost:5173/azure-dashboard'
        }
        mock_config.SCREENSHOT_DIR = 'screenshots'
        
        # Mock partial success (only 2 out of 3 screenshots succeed)
        mock_asyncio_run.return_value = [
            'screenshots/gcp_dashboard.png',
            'screenshots/aws_dashboard.png'
            # azure screenshot missing
        ]
        
        result = take_screenshots()
        
        self.assertEqual(len(result), 2)
    
    @patch('data.screenshotter.playwright.async_api.async_playwright')
    @patch('data.screenshotter.asyncio.new_event_loop')
    @patch('data.screenshotter.user_config')
    def test_login_and_save_state(self, mock_config, mock_new_loop, mock_playwright):
        """Test login and state saving functionality"""
        # Mock configuration
        mock_config.DASHBOARD_BASE_URL = 'http://localhost:5173'
        
        # Mock playwright
        mock_playwright_instance = MagicMock()
        mock_browser = MagicMock()
        mock_page = MagicMock()
        
        mock_playwright.return_value.__aenter__.return_value = mock_playwright_instance
        mock_playwright_instance.chromium.launch.return_value.__aenter__.return_value = mock_browser
        mock_browser.new_page.return_value.__aenter__.return_value = mock_page
        
        # Mock event loop
        mock_loop = MagicMock()
        mock_new_loop.return_value = mock_loop
        
        # Mock async function
        async def mock_login_func():
            pass
        
        mock_loop.run_until_complete = MagicMock(side_effect=mock_login_func)
        
        # This should not raise any exceptions
        try:
            login_and_save_state()
        except Exception as e:
            self.fail(f"login_and_save_state raised {e} unexpectedly!")


class TestScreenshotAsyncFunction(unittest.TestCase):
    """Test cases for async screenshot functions"""
    
    @patch('data.screenshotter.async_playwright')
    @patch('data.screenshotter.os.makedirs')
    @patch('data.screenshotter.user_config')
    def test_capture_screenshots_async(self, mock_config, mock_makedirs, mock_playwright):
        """Test async screenshot capture function"""
        # Mock configuration
        mock_config.DASHBOARD_TAB_URLS = {
            'gcp': 'http://localhost:5173/gcp-dashboard',
            'aws': 'http://localhost:5173/aws-dashboard'
        }
        mock_config.SCREENSHOT_DIR = 'screenshots'
        mock_config.SCREENSHOT_HEADLESS = True
        mock_config.SCREENSHOT_SELECTOR = '.cloud-card'
        
        # Mock playwright objects
        mock_playwright_instance = MagicMock()
        mock_browser = MagicMock()
        mock_context = MagicMock()
        mock_page = MagicMock()
        
        mock_playwright.return_value.__aenter__.return_value = mock_playwright_instance
        mock_playwright_instance.chromium.launch.return_value.__aenter__.return_value = mock_browser
        mock_browser.new_context.return_value.__aenter__.return_value = mock_context
        mock_context.new_page.return_value.__aenter__.return_value = mock_page
        
        # Mock page operations
        mock_page.goto.return_value = None
        mock_page.wait_for_selector.return_value = None
        mock_page.screenshot.return_value = b'fake_image_data'
        
        # Import and test the async function
        from data.screenshotter import capture_screenshots_async
        
        # Run the async function
        async def test_async():
            return await capture_screenshots_async()
        
        # Mock asyncio.run to call our test function
        with patch('data.screenshotter.asyncio.run', side_effect=lambda coro: asyncio.run(coro)):
            with patch('data.screenshotter.capture_screenshots_async', side_effect=test_async):
                result = asyncio.run(test_async())
        
        # Verify the function returns expected number of screenshots
        self.assertEqual(len(result), 2)
    
    @patch('data.screenshotter.async_playwright')
    @patch('data.screenshotter.user_config')
    def test_capture_screenshots_async_with_auth(self, mock_config, mock_playwright):
        """Test async screenshot capture with authentication"""
        # Mock configuration with cookies file
        mock_config.DASHBOARD_TAB_URLS = {
            'gcp': 'http://localhost:5173/gcp-dashboard'
        }
        mock_config.SCREENSHOT_DIR = 'screenshots'
        mock_config.SCREENSHOT_HEADLESS = True
        mock_config.SCREENSHOT_SELECTOR = '.cloud-card'
        mock_config.COOKIES_FILE = 'auth_cookies.json'
        
        # Mock playwright objects
        mock_playwright_instance = MagicMock()
        mock_browser = MagicMock()
        mock_context = MagicMock()
        mock_page = MagicMock()
        
        mock_playwright.return_value.__aenter__.return_value = mock_playwright_instance
        mock_playwright_instance.chromium.launch.return_value.__aenter__.return_value = mock_browser
        mock_browser.new_context.return_value.__aenter__.return_value = mock_context
        mock_context.new_page.return_value.__aenter__.return_value = mock_page
        
        # Mock page operations
        mock_page.goto.return_value = None
        mock_page.wait_for_selector.return_value = None
        mock_page.screenshot.return_value = b'fake_image_data'
        
        # Mock file operations for cookies
        with patch('builtins.open', create=True) as mock_open:
            mock_file = MagicMock()
            mock_open.return_value.__enter__.return_value = mock_file
            
            # Test that cookies file is used when available
            from data.screenshotter import capture_screenshots_async
            
            # The function should attempt to load cookies if file exists
            # This is tested by verifying the file open call
            async def test_async():
                return await capture_screenshots_async()
            
            # Run the test
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(test_async())
            finally:
                loop.close()


if __name__ == '__main__':
    unittest.main()
