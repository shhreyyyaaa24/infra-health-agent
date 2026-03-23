"""
Core AI Agent for Infrastructure Health Monitoring
Intelligent agent that makes autonomous decisions and adapts to patterns
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from .decision import DecisionEngine
from .analysis import DataAnalyzer
from .learning import LearningSystem
from .custom_actions import CustomActionHandler
from config import DIRECTOR_CONFIG, EMAIL_CONFIG
from data.fetcher import fetch_all_environment_data
from data.screenshotter import take_screenshots
from email_module.email_composer import build_html_email
from email_module.mailer import send_email_with_attachments


@dataclass
class AgentAction:
    """Represents an action taken by the AI agent"""
    action_type: str
    description: str
    timestamp: datetime
    confidence: float
    data: Dict[str, Any]


@dataclass
class AgentDecision:
    """Represents a decision made by the AI agent"""
    decision_type: str
    reasoning: str
    confidence: float
    actions: List[AgentAction]
    timestamp: datetime


class InfrastructureHealthAgent:
    """
    AI Agent that monitors infrastructure health and makes intelligent decisions
    """
    
    def __init__(self, learning_enabled: bool = True):
        self.logger = logging.getLogger(__name__)
        self.decision_engine = DecisionEngine()
        self.analyzer = DataAnalyzer()
        self.learning_system = LearningSystem() if learning_enabled else None
        
        # Agent state
        self.history: List[AgentDecision] = []
        self.current_context: Dict[str, Any] = {}
        self.last_analysis: Optional[Dict] = None
        
        # Agent capabilities
        self.capabilities = [
            "anomaly_detection",
            "trend_analysis", 
            "predictive_alerts",
            "adaptive_reporting",
            "autonomous_decision_making",
            "pattern_learning"
        ]
        
        self.logger.info("AI Agent initialized with capabilities: %s", self.capabilities)
    
    def assess_situation(self) -> Dict[str, Any]:
        """
        Assess the current infrastructure situation
        """
        self.logger.info("🤖 AI Agent assessing current situation...")
        
        # Gather data
        infrastructure_data = fetch_all_environment_data()
        
        # Analyze data with AI
        analysis = self.analyzer.analyze_infrastructure(infrastructure_data)
        
        # Learn from patterns if enabled
        if self.learning_system:
            patterns = self.learning_system.identify_patterns(infrastructure_data)
            analysis['patterns'] = patterns
            
            # Predict future issues
            predictions = self.learning_system.predict_issues(infrastructure_data)
            analysis['predictions'] = predictions
        
        self.last_analysis = analysis
        self.current_context = {
            'analysis': analysis,
            'timestamp': datetime.now(),
            'data_summary': self._create_data_summary(infrastructure_data)
        }
        
        return analysis
    
    def make_decisions(self, situation: Dict[str, Any]) -> List[AgentDecision]:
        """
        Make intelligent decisions based on the current situation
        """
        self.logger.info("🧠 AI Agent making intelligent decisions...")
        
        decisions = []
        
        # Decision: Alert severity assessment
        severity_decision = self.decision_engine.assess_alert_severity(situation)
        if severity_decision['should_alert']:
            decision = AgentDecision(
                decision_type="alert_severity",
                reasoning=severity_decision['reasoning'],
                confidence=severity_decision['confidence'],
                actions=[],
                timestamp=datetime.now()
            )
            decisions.append(decision)
        
        # Decision: Reporting strategy
        reporting_decision = self.decision_engine.determine_reporting_strategy(situation)
        decision = AgentDecision(
            decision_type="reporting_strategy",
            reasoning=reporting_decision['reasoning'],
            confidence=reporting_decision['confidence'],
            actions=[],
            timestamp=datetime.now()
        )
        decisions.append(decision)
        
        # Decision: Immediate actions needed
        if situation.get('critical_issues'):
            action_decision = self.decision_engine.recommend_immediate_actions(situation)
            decision = AgentDecision(
                decision_type="immediate_actions",
                reasoning=action_decision['reasoning'],
                confidence=action_decision['confidence'],
                actions=[],
                timestamp=datetime.now()
            )
            decisions.append(decision)
        
        # Store decisions in history
        self.history.extend(decisions)
        
        return decisions
    
    def execute_actions(self, decisions: List[AgentDecision]) -> List[AgentAction]:
        """
        Execute actions based on decisions
        """
        self.logger.info("⚡ AI Agent executing actions...")
        
        actions = []
        
        for decision in decisions:
            if decision.decision_type == "alert_severity":
                action = self._handle_alert_severity(decision)
                actions.append(action)
            
            elif decision.decision_type == "reporting_strategy":
                action = self._handle_reporting_strategy(decision)
                actions.append(action)
            
            elif decision.decision_type == "immediate_actions":
                action_list = self._handle_immediate_actions(decision)
                actions.extend(action_list)
        
        # Update decisions with executed actions
        for decision in decisions:
            decision.actions = [a for a in actions if a.timestamp >= decision.timestamp]
        
        return actions
    
    def _handle_alert_severity(self, decision: AgentDecision) -> AgentAction:
        """Handle alert severity decision"""
        severity = self.last_analysis.get('overall_severity', 'medium')
        
        if severity == 'critical':
            # Send immediate high-priority alert
            action = AgentAction(
                action_type="immediate_alert",
                description="Sent immediate critical alert to director",
                timestamp=datetime.now(),
                confidence=decision.confidence,
                data={'severity': severity, 'recipients': DIRECTOR_CONFIG['email']}
            )
        elif severity == 'high':
            # Schedule urgent report
            action = AgentAction(
                action_type="urgent_report",
                description="Scheduled urgent infrastructure report",
                timestamp=datetime.now(),
                confidence=decision.confidence,
                data={'severity': severity}
            )
        else:
            # Standard reporting
            action = AgentAction(
                action_type="standard_report",
                description="Generated standard infrastructure report",
                timestamp=datetime.now(),
                confidence=decision.confidence,
                data={'severity': severity}
            )
        
        return action
    
    def _handle_reporting_strategy(self, decision: AgentDecision) -> AgentAction:
        """Handle reporting strategy decision"""
        # Take screenshots for visual context
        screenshots = take_screenshots()
        
        # Build intelligent email content
        html_content = self._generate_intelligent_email_content()
        
        # Send email via custom action handler (SMTP + cron support)
        handler = CustomActionHandler()
        success = handler.send_report_email(html_body=html_content, screenshot_paths=screenshots, all_data=self.last_analysis)

        action = AgentAction(
            action_type="intelligent_report",
            description=f"Sent AI-enhanced report with {len(screenshots)} screenshots",
            timestamp=datetime.now(),
            confidence=decision.confidence,
            data={
                'screenshots_count': len(screenshots),
                'email_sent': success,
                'content_type': 'ai_enhanced'
            }
        )

        return action
    
    def _handle_immediate_actions(self, decision: AgentDecision) -> List[AgentAction]:
        """Handle immediate actions for critical issues"""
        actions = []
        
        critical_issues = self.last_analysis.get('critical_issues', [])
        
        for issue in critical_issues:
            action = AgentAction(
                action_type="immediate_action",
                description=f"Immediate action recommended for {issue['project']}",
                timestamp=datetime.now(),
                confidence=decision.confidence,
                data={
                    'issue': issue,
                    'recommended_action': issue.get('recommended_action'),
                    'urgency': 'critical'
                }
            )
            actions.append(action)
        
        return actions
    
    def _generate_intelligent_email_content(self) -> str:
        """Generate AI-enhanced email content"""
        infrastructure_data = fetch_all_environment_data()
        
        # Add AI insights to the standard email
        base_html = build_html_email(infrastructure_data)
        
        # Add AI analysis section
        ai_insights = self._generate_ai_insights_section()
        
        # Insert AI insights before the summary
        html_with_ai = base_html.replace(
            '<div style="background-color: #f8f9fa;',
            ai_insights + '<div style="background-color: #f8f9fa;'
        )
        
        return html_with_ai
    
    def _generate_ai_insights_section(self) -> str:
        """Generate AI insights section for email"""
        if not self.last_analysis:
            return ""
        
        insights_html = """
        <div style="background-color: #e8f4fd; padding: 15px; border-radius: 5px; margin-bottom: 20px; border-left: 4px solid #2196F3;">
            <h3>🤖 AI Agent Insights</h3>
        """
        
        # Add anomaly detection results
        if self.last_analysis.get('anomalies'):
            insights_html += "<p><strong>🚨 Anomalies Detected:</strong></p><ul>"
            for anomaly in self.last_analysis['anomalies']:
                insights_html += f"<li>{anomaly['description']}</li>"
            insights_html += "</ul>"
        
        # Add trend analysis
        if self.last_analysis.get('trends'):
            insights_html += "<p><strong>📈 Trend Analysis:</strong></p><ul>"
            for trend in self.last_analysis['trends']:
                insights_html += f"<li>{trend['description']}</li>"
            insights_html += "</ul>"
        
        # Add predictions if available
        if self.last_analysis.get('predictions'):
            insights_html += "<p><strong>🔮 Predictions:</strong></p><ul>"
            for prediction in self.last_analysis['predictions']:
                insights_html += f"<li>{prediction['description']} (Confidence: {prediction['confidence']}%)</li>"
            insights_html += "</ul>"
        
        # Add recommendations
        if self.last_analysis.get('recommendations'):
            insights_html += "<p><strong>💡 Recommendations:</strong></p><ul>"
            for rec in self.last_analysis['recommendations']:
                insights_html += f"<li>{rec}</li>"
            insights_html += "</ul>"
        
        insights_html += "</div>"
        
        return insights_html
    
    def _create_data_summary(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a summary of the current data"""
        total_projects = sum(len(projects) for projects in data.values())
        
        status_counts = {"HEALTHY": 0, "MEDIUM": 0, "SEVERE": 0}
        for projects in data.values():
            for project in projects:
                status_counts[project['status']] += 1
        
        return {
            'total_projects': total_projects,
            'status_distribution': status_counts,
            'environments': list(data.keys()),
            'timestamp': datetime.now().isoformat()
        }
    
    def run_intelligent_cycle(self) -> Dict[str, Any]:
        """
        Run a complete intelligent monitoring cycle
        """
        self.logger.info("🚀 Starting AI Agent intelligent monitoring cycle...")
        
        cycle_start = datetime.now()
        
        # 1. Assess situation
        situation = self.assess_situation()
        
        # 2. Make decisions
        decisions = self.make_decisions(situation)
        
        # 3. Execute actions
        actions = self.execute_actions(decisions)
        
        # 4. Learn and improve
        if self.learning_system:
            self.learning_system.update_knowledge(situation, decisions, actions)
        
        cycle_end = datetime.now()
        cycle_duration = (cycle_end - cycle_start).total_seconds()
        
        # Summary
        summary = {
            'cycle_start': cycle_start.isoformat(),
            'cycle_end': cycle_end.isoformat(),
            'duration_seconds': cycle_duration,
            'decisions_made': len(decisions),
            'actions_executed': len(actions),
            'situation_assessment': situation,
            'ai_insights': self.last_analysis
        }
        
        self.logger.info(f"✅ AI Agent cycle completed in {cycle_duration:.2f}s")
        return summary
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get current agent status and statistics"""
        return {
            'agent_type': 'AI Infrastructure Health Agent',
            'capabilities': self.capabilities,
            'decisions_history_count': len(self.history),
            'learning_enabled': self.learning_system is not None,
            'last_analysis': self.last_analysis,
            'current_context': self.current_context,
            'uptime': datetime.now().isoformat()
        }
