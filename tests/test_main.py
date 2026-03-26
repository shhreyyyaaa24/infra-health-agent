"""
Test cases for main.py - Infrastructure Health Agent
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import argparse

# Add the parent directory to the path to import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import InfrastructureHealthMonitor, create_parser, main


class TestInfrastructureHealthMonitor(unittest.TestCase):
    """Test cases for InfrastructureHealthMonitor class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.monitor = InfrastructureHealthMonitor()
    
    def test_init(self):
        """Test monitor initialization"""
        self.assertIsNone(self.monitor.ai_agent)
    
    @patch('main.fetch_all_environment_data')
    @patch('main.get_summary_stats')
    @patch('main.take_screenshots')
    @patch('main.build_html_email')
    @patch('main.send_email_with_attachments')
    def test_run_health_check_success(self, mock_send_email, mock_build_email, 
                                    mock_screenshots, mock_stats, mock_fetch_data):
        """Test successful health check run"""
        # Mock data
        mock_fetch_data.return_value = [{'name': 'test-project', 'status': 'HEALTHY'}]
        mock_stats.return_value = {
            'total_projects': 1,
            'status_counts': {'HEALTHY': 1, 'MEDIUM': 0, 'SEVERE': 0}
        }
        mock_screenshots.return_value = ['screenshot.png']
        mock_build_email.return_value = '<html>Report</html>'
        mock_send_email.return_value = True
        
        result = self.monitor.run_health_check(dry_run=False)
        
        self.assertTrue(result)
        mock_fetch_data.assert_called_once()
        mock_screenshots.assert_called_once()
        mock_build_email.assert_called_once()
        mock_send_email.assert_called_once()
    
    @patch('main.fetch_all_environment_data')
    def test_run_health_check_no_data(self, mock_fetch_data):
        """Test health check when no data is fetched"""
        mock_fetch_data.return_value = None
        
        result = self.monitor.run_health_check()
        
        self.assertFalse(result)
        mock_fetch_data.assert_called_once()
    
    @patch('main.fetch_all_environment_data')
    @patch('main.get_summary_stats')
    @patch('main.take_screenshots')
    @patch('main.build_html_email')
    @patch('main.preview_email_html')
    def test_run_health_check_dry_run(self, mock_preview, mock_build_email,
                                    mock_screenshots, mock_stats, mock_fetch_data):
        """Test health check in dry run mode"""
        mock_fetch_data.return_value = [{'name': 'test-project', 'status': 'HEALTHY'}]
        mock_stats.return_value = {
            'total_projects': 1,
            'status_counts': {'HEALTHY': 1, 'MEDIUM': 0, 'SEVERE': 0}
        }
        mock_screenshots.return_value = ['screenshot.png']
        mock_build_email.return_value = '<html>Report</html>'
        
        result = self.monitor.run_health_check(dry_run=True)
        
        self.assertTrue(result)
        mock_preview.assert_called_once()
    
    @patch('main.AI_AGENT_AVAILABLE', False)
    def test_run_ai_monitoring_unavailable(self):
        """Test AI monitoring when AI agent is not available"""
        result = self.monitor.run_ai_monitoring()
        
        self.assertFalse(result)
    
    @patch('main.AI_AGENT_AVAILABLE', True)
    @patch('main.InfrastructureHealthAgent')
    def test_run_ai_monitoring_success(self, mock_agent_class):
        """Test successful AI monitoring run"""
        mock_agent = MagicMock()
        mock_agent.run_intelligent_cycle.return_value = {
            'duration_seconds': 5.0,
            'decisions_made': 3,
            'actions_executed': 2,
            'ai_insights': {
                'anomalies': [],
                'trends': [],
                'critical_issues': [],
                'recommendations': [],
                'predictions': []
            }
        }
        mock_agent_class.return_value = mock_agent
        
        result = self.monitor.run_ai_monitoring()
        
        self.assertTrue(result)
        mock_agent.run_intelligent_cycle.assert_called_once()
    
    @patch('main.AI_AGENT_AVAILABLE', False)
    def test_run_scheduler_unavailable(self):
        """Test scheduler when AI agent is not available"""
        result = self.monitor.run_scheduler()
        
        self.assertFalse(result)
    
    @patch('main.AI_AGENT_AVAILABLE', True)
    @patch('main.EMAIL_CRON_SCHEDULE', {'enabled': False})
    def test_run_scheduler_disabled(self):
        """Test scheduler when disabled in config"""
        result = self.monitor.run_scheduler()
        
        self.assertFalse(result)
    
    @patch('main.AI_AGENT_AVAILABLE', True)
    @patch('main.EMAIL_CRON_SCHEDULE', {'enabled': True, 'send_time': 'invalid'})
    def test_run_scheduler_invalid_time(self):
        """Test scheduler with invalid time format"""
        result = self.monitor.run_scheduler()
        
        self.assertFalse(result)


class TestArgumentParser(unittest.TestCase):
    """Test cases for command line argument parser"""
    
    def test_create_parser(self):
        """Test parser creation"""
        parser = create_parser()
        self.assertIsInstance(parser, argparse.ArgumentParser)
    
    def test_parser_default_args(self):
        """Test parser with default arguments"""
        parser = create_parser()
        args = parser.parse_args([])
        
        self.assertFalse(args.dry_run)
        self.assertFalse(args.ai_agent)
        self.assertFalse(args.schedule)
    
    def test_parser_with_dry_run(self):
        """Test parser with dry-run argument"""
        parser = create_parser()
        args = parser.parse_args(['--dry-run'])
        
        self.assertTrue(args.dry_run)
        self.assertFalse(args.ai_agent)
        self.assertFalse(args.schedule)
    
    def test_parser_with_ai_agent(self):
        """Test parser with ai-agent argument"""
        parser = create_parser()
        args = parser.parse_args(['--ai-agent'])
        
        self.assertFalse(args.dry_run)
        self.assertTrue(args.ai_agent)
        self.assertFalse(args.schedule)
    
    def test_parser_with_schedule(self):
        """Test parser with schedule argument"""
        parser = create_parser()
        args = parser.parse_args(['--schedule'])
        
        self.assertFalse(args.dry_run)
        self.assertFalse(args.ai_agent)
        self.assertTrue(args.schedule)


class TestMainFunction(unittest.TestCase):
    """Test cases for main function"""
    
    @patch('main.create_parser')
    @patch('main.InfrastructureHealthMonitor')
    @patch('sys.argv', ['main.py'])
    def test_main_default_mode(self, mock_monitor_class, mock_parser_class):
        """Test main function in default mode"""
        mock_parser = MagicMock()
        mock_parser_class.return_value = mock_parser
        mock_args = MagicMock()
        mock_args.dry_run = False
        mock_args.ai_agent = False
        mock_args.schedule = False
        mock_parser.parse_args.return_value = mock_args
        
        mock_monitor = MagicMock()
        mock_monitor.run_health_check.return_value = True
        mock_monitor_class.return_value = mock_monitor
        
        with patch('sys.exit') as mock_exit:
            main()
            mock_exit.assert_called_with(0)
    
    @patch('main.create_parser')
    @patch('main.InfrastructureHealthMonitor')
    @patch('sys.argv', ['main.py', '--ai-agent'])
    def test_main_ai_agent_mode(self, mock_monitor_class, mock_parser_class):
        """Test main function in AI agent mode"""
        mock_parser = MagicMock()
        mock_parser_class.return_value = mock_parser
        mock_args = MagicMock()
        mock_args.dry_run = False
        mock_args.ai_agent = True
        mock_args.schedule = False
        mock_parser.parse_args.return_value = mock_args
        
        mock_monitor = MagicMock()
        mock_monitor.run_ai_monitoring.return_value = True
        mock_monitor_class.return_value = mock_monitor
        
        with patch('sys.exit') as mock_exit:
            main()
            mock_exit.assert_called_with(0)
    
    @patch('main.create_parser')
    @patch('main.InfrastructureHealthMonitor')
    @patch('sys.argv', ['main.py', '--schedule'])
    def test_main_schedule_mode(self, mock_monitor_class, mock_parser_class):
        """Test main function in schedule mode"""
        mock_parser = MagicMock()
        mock_parser_class.return_value = mock_parser
        mock_args = MagicMock()
        mock_args.dry_run = False
        mock_args.ai_agent = False
        mock_args.schedule = True
        mock_parser.parse_args.return_value = mock_args
        
        mock_monitor = MagicMock()
        mock_monitor.run_scheduler.return_value = True
        mock_monitor_class.return_value = mock_monitor
        
        with patch('sys.exit') as mock_exit:
            main()
            mock_exit.assert_called_with(0)


if __name__ == '__main__':
    unittest.main()
