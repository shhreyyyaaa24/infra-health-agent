"""
Test cases for data.fetcher module
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import requests

# Add the parent directory to the path to import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.fetcher import fetch_all_environment_data, get_summary_stats


class TestDataFetcher(unittest.TestCase):
    """Test cases for data fetching functionality"""
    
    @patch('data.fetcher.requests.get')
    @patch('data.fetcher.user_config')
    def test_fetch_all_environment_data_success(self, mock_config, mock_get):
        """Test successful data fetching"""
        # Mock configuration
        mock_config.API_ENDPOINT = "https://api.example.com/projects"
        mock_config.USE_WINDOWS_AUTH = False
        mock_config.BASIC_AUTH_USER = "testuser"
        mock_config.BASIC_AUTH_PASS = "testpass"
        
        # Mock API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {'name': 'project1', 'status': 'HEALTHY', 'environment': 'prod'},
            {'name': 'project2', 'status': 'MEDIUM', 'environment': 'dev'}
        ]
        mock_get.return_value = mock_response
        
        result = fetch_all_environment_data()
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['name'], 'project1')
        self.assertEqual(result[1]['status'], 'MEDIUM')
        mock_get.assert_called_once()
    
    @patch('data.fetcher.requests.get')
    @patch('data.fetcher.user_config')
    def test_fetch_all_environment_data_api_error(self, mock_config, mock_get):
        """Test data fetching with API error"""
        mock_config.API_ENDPOINT = "https://api.example.com/projects"
        mock_config.USE_WINDOWS_AUTH = False
        mock_config.BASIC_AUTH_USER = ""
        mock_config.BASIC_AUTH_PASS = ""
        
        # Mock API error response
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_get.return_value = mock_response
        
        result = fetch_all_environment_data()
        
        self.assertIsNone(result)
    
    @patch('data.fetcher.requests.get')
    @patch('data.fetcher.user_config')
    def test_fetch_all_environment_data_network_error(self, mock_config, mock_get):
        """Test data fetching with network error"""
        mock_config.API_ENDPOINT = "https://api.example.com/projects"
        mock_config.USE_WINDOWS_AUTH = False
        mock_config.BASIC_AUTH_USER = ""
        mock_config.BASIC_AUTH_PASS = ""
        
        # Mock network error
        mock_get.side_effect = requests.ConnectionError("Network error")
        
        result = fetch_all_environment_data()
        
        self.assertIsNone(result)
    
    @patch('data.fetcher.requests.get')
    @patch('data.fetcher.user_config')
    def test_fetch_all_environment_data_windows_auth(self, mock_config, mock_get):
        """Test data fetching with Windows authentication"""
        mock_config.API_ENDPOINT = "https://api.example.com/projects"
        mock_config.USE_WINDOWS_AUTH = True
        mock_config.BASIC_AUTH_USER = ""
        mock_config.BASIC_AUTH_PASS = ""
        
        # Mock API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{'name': 'project1', 'status': 'HEALTHY'}]
        mock_get.return_value = mock_response
        
        result = fetch_all_environment_data()
        
        self.assertEqual(len(result), 1)
        mock_get.assert_called_once()


class TestSummaryStats(unittest.TestCase):
    """Test cases for summary statistics functionality"""
    
    def test_get_summary_stats_empty_data(self):
        """Test summary stats with empty data"""
        result = get_summary_stats([])
        
        self.assertEqual(result['total_projects'], 0)
        self.assertEqual(result['status_counts']['HEALTHY'], 0)
        self.assertEqual(result['status_counts']['MEDIUM'], 0)
        self.assertEqual(result['status_counts']['SEVERE'], 0)
    
    def test_get_summary_stats_mixed_data(self):
        """Test summary stats with mixed status data"""
        test_data = [
            {'name': 'project1', 'status': 'HEALTHY'},
            {'name': 'project2', 'status': 'MEDIUM'},
            {'name': 'project3', 'status': 'SEVERE'},
            {'name': 'project4', 'status': 'HEALTHY'},
            {'name': 'project5', 'status': 'MEDIUM'}
        ]
        
        result = get_summary_stats(test_data)
        
        self.assertEqual(result['total_projects'], 5)
        self.assertEqual(result['status_counts']['HEALTHY'], 2)
        self.assertEqual(result['status_counts']['MEDIUM'], 2)
        self.assertEqual(result['status_counts']['SEVERE'], 1)
    
    def test_get_summary_stats_all_healthy(self):
        """Test summary stats with all healthy projects"""
        test_data = [
            {'name': 'project1', 'status': 'HEALTHY'},
            {'name': 'project2', 'status': 'HEALTHY'},
            {'name': 'project3', 'status': 'HEALTHY'}
        ]
        
        result = get_summary_stats(test_data)
        
        self.assertEqual(result['total_projects'], 3)
        self.assertEqual(result['status_counts']['HEALTHY'], 3)
        self.assertEqual(result['status_counts']['MEDIUM'], 0)
        self.assertEqual(result['status_counts']['SEVERE'], 0)
    
    def test_get_summary_stats_unknown_status(self):
        """Test summary stats with unknown status"""
        test_data = [
            {'name': 'project1', 'status': 'UNKNOWN'},
            {'name': 'project2', 'status': 'HEALTHY'}
        ]
        
        result = get_summary_stats(test_data)
        
        self.assertEqual(result['total_projects'], 2)
        self.assertEqual(result['status_counts']['HEALTHY'], 1)
        # Unknown status should not be counted
        self.assertEqual(result['status_counts']['MEDIUM'], 0)
        self.assertEqual(result['status_counts']['SEVERE'], 0)


if __name__ == '__main__':
    unittest.main()
