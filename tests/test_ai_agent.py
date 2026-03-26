"""
Test cases for AI Agent functionality
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the parent directory to the path to import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestAIAgent(unittest.TestCase):
    """Test cases for AI Agent functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Mock AI Agent availability
        self.ai_agent_patcher = patch('main.AI_AGENT_AVAILABLE', True)
        self.ai_agent_patcher.start()
    
    def tearDown(self):
        """Clean up after tests"""
        self.ai_agent_patcher.stop()
    
    @patch('main.InfrastructureHealthAgent')
    def test_ai_agent_initialization(self, mock_agent_class):
        """Test AI Agent initialization"""
        mock_agent = MagicMock()
        mock_agent_class.return_value = mock_agent
        
        from main import InfrastructureHealthMonitor
        monitor = InfrastructureHealthMonitor()
        
        # Test AI monitoring with learning enabled
        monitor.run_ai_monitoring()
        
        mock_agent_class.assert_called_once_with(learning_enabled=True)
    
    @patch('main.InfrastructureHealthAgent')
    def test_ai_agent_cycle_execution(self, mock_agent_class):
        """Test AI Agent cycle execution"""
        mock_agent = MagicMock()
        mock_agent.run_intelligent_cycle.return_value = {
            'duration_seconds': 10.5,
            'decisions_made': 5,
            'actions_executed': 3,
            'ai_insights': {
                'anomalies': [
                    {'description': 'High CPU usage', 'severity': 'medium'}
                ],
                'trends': [
                    {'description': 'Memory usage increasing', 'confidence': 85}
                ],
                'critical_issues': [
                    {'description': 'Database connection failed', 'severity': 'high'}
                ],
                'recommendations': [
                    {'description': 'Scale up resources', 'priority': 'high'}
                ],
                'predictions': [
                    {'description': 'Potential downtime in 2 hours', 'confidence': 75}
                ]
            }
        }
        mock_agent_class.return_value = mock_agent
        
        from main import InfrastructureHealthMonitor
        monitor = InfrastructureHealthMonitor()
        
        result = monitor.run_ai_monitoring()
        
        self.assertTrue(result)
        mock_agent.run_intelligent_cycle.assert_called_once()
    
    @patch('main.InfrastructureHealthAgent')
    def test_ai_agent_empty_insights(self, mock_agent_class):
        """Test AI Agent with empty insights"""
        mock_agent = MagicMock()
        mock_agent.run_intelligent_cycle.return_value = {
            'duration_seconds': 5.0,
            'decisions_made': 0,
            'actions_executed': 0,
            'ai_insights': {}
        }
        mock_agent_class.return_value = mock_agent
        
        from main import InfrastructureHealthMonitor
        monitor = InfrastructureHealthMonitor()
        
        result = monitor.run_ai_monitoring()
        
        self.assertTrue(result)
    
    @patch('main.InfrastructureHealthAgent')
    def test_ai_agent_error_handling(self, mock_agent_class):
        """Test AI Agent error handling"""
        mock_agent = MagicMock()
        mock_agent.run_intelligent_cycle.side_effect = Exception("AI Agent error")
        mock_agent_class.return_value = mock_agent
        
        from main import InfrastructureHealthMonitor
        monitor = InfrastructureHealthMonitor()
        
        # Should handle the error gracefully
        with self.assertRaises(Exception):
            monitor.run_ai_monitoring()
    
    @patch('main.InfrastructureHealthAgent')
    def test_ai_agent_dry_run_mode(self, mock_agent_class):
        """Test AI Agent in dry run mode"""
        mock_agent = MagicMock()
        mock_agent.run_intelligent_cycle.return_value = {
            'duration_seconds': 8.0,
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
        
        from main import InfrastructureHealthMonitor
        monitor = InfrastructureHealthMonitor()
        
        result = monitor.run_ai_monitoring(dry_run=True)
        
        self.assertTrue(result)
        # Dry run should not affect the AI processing
        mock_agent.run_intelligent_cycle.assert_called_once()


class TestAIAgentModules(unittest.TestCase):
    """Test cases for individual AI Agent modules"""
    
    @patch('main.AI_AGENT_AVAILABLE', True)
    def test_analysis_module_import(self):
        """Test analysis module import and functionality"""
        try:
            from ai_agent.analysis.analyzer import InfrastructureAnalyzer
            from ai_agent.analysis.anomaly_detector import AnomalyDetector
            from ai_agent.analysis.trend_analyzer import TrendAnalyzer
            
            # Test module initialization
            analyzer = InfrastructureAnalyzer()
            detector = AnomalyDetector()
            trend_analyzer = TrendAnalyzer()
            
            self.assertIsNotNone(analyzer)
            self.assertIsNotNone(detector)
            self.assertIsNotNone(trend_analyzer)
            
        except ImportError:
            # Skip test if modules are not available
            self.skipTest("AI Agent analysis modules not available")
    
    @patch('main.AI_AGENT_AVAILABLE', True)
    def test_decision_module_import(self):
        """Test decision module import and functionality"""
        try:
            from ai_agent.decision.action_recommender import ActionRecommender
            from ai_agent.decision.alert_evaluator import AlertEvaluator
            from ai_agent.decision.decision_engine import DecisionEngine
            
            # Test module initialization
            recommender = ActionRecommender()
            evaluator = AlertEvaluator()
            engine = DecisionEngine()
            
            self.assertIsNotNone(recommender)
            self.assertIsNotNone(evaluator)
            self.assertIsNotNone(engine)
            
        except ImportError:
            # Skip test if modules are not available
            self.skipTest("AI Agent decision modules not available")
    
    @patch('main.AI_AGENT_AVAILABLE', True)
    def test_learning_module_import(self):
        """Test learning module import and functionality"""
        try:
            from ai_agent.learning.learning import LearningEngine
            from ai_agent.learning.pattern_matcher import PatternMatcher
            from ai_agent.learning.predictor import Predictor
            
            # Test module initialization
            learning_engine = LearningEngine()
            pattern_matcher = PatternMatcher()
            predictor = Predictor()
            
            self.assertIsNotNone(learning_engine)
            self.assertIsNotNone(pattern_matcher)
            self.assertIsNotNone(predictor)
            
        except ImportError:
            # Skip test if modules are not available
            self.skipTest("AI Agent learning modules not available")


class TestCustomActions(unittest.TestCase):
    """Test cases for custom actions functionality"""
    
    @patch('main.AI_AGENT_AVAILABLE', True)
    @patch('main.CustomActionHandler')
    def test_scheduler_custom_action(self, mock_handler_class):
        """Test scheduler custom action"""
        mock_handler = MagicMock()
        mock_handler_class.return_value = mock_handler
        
        from main import InfrastructureHealthMonitor
        monitor = InfrastructureHealthMonitor()
        
        with patch('main.EMAIL_CRON_SCHEDULE', {
            'enabled': True,
            'day_of_week': 'fri',
            'send_time': '09:00',
            'timezone': None
        }):
            result = monitor.run_scheduler()
            
            self.assertTrue(result)
            mock_handler.schedule_report_cron.assert_called_once()
    
    @patch('main.AI_AGENT_AVAILABLE', True)
    @patch('main.CustomActionHandler')
    def test_scheduler_stop_functionality(self, mock_handler_class):
        """Test scheduler stop functionality"""
        mock_handler = MagicMock()
        mock_handler_class.return_value = mock_handler
        
        # Simulate KeyboardInterrupt
        def mock_schedule_side_effect(*args, **kwargs):
            raise KeyboardInterrupt()
        
        mock_handler.schedule_report_cron.side_effect = mock_schedule_side_effect
        
        from main import InfrastructureHealthMonitor
        monitor = InfrastructureHealthMonitor()
        
        with patch('main.EMAIL_CRON_SCHEDULE', {
            'enabled': True,
            'day_of_week': 'fri',
            'send_time': '09:00',
            'timezone': None
        }):
            result = monitor.run_scheduler()
            
            # Should handle KeyboardInterrupt gracefully
            self.assertTrue(result)
            mock_handler.stop_scheduler.assert_called_once()


if __name__ == '__main__':
    unittest.main()
