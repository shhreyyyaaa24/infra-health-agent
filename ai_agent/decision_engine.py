"""
Decision Engine for AI Agent
Handles intelligent decision-making based on data analysis
"""

import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class DecisionCriteria:
    """Criteria for making decisions"""
    severity_threshold: float
    confidence_threshold: float
    risk_tolerance: float
    priority_weights: Dict[str, float]


class DecisionEngine:
    """
    Intelligent decision-making engine for infrastructure monitoring
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Decision criteria
        self.criteria = DecisionCriteria(
            severity_threshold=0.7,
            confidence_threshold=0.6,
            risk_tolerance=0.5,
            priority_weights={
                'critical': 1.0,
                'high': 0.8,
                'medium': 0.5,
                'low': 0.2
            }
        )
        
        # Decision rules
        self.decision_rules = {
            'alert_severity': self._evaluate_alert_severity,
            'reporting_strategy': self._evaluate_reporting_strategy,
            'immediate_actions': self._evaluate_immediate_actions,
            'escalation': self._evaluate_escalation_needs
        }
        
        self.logger.info("Decision Engine initialized with intelligent criteria")
    
    def assess_alert_severity(self, situation: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess the severity of alerts and decide on response level
        """
        self.logger.info("🎯 Assessing alert severity...")
        
        analysis = situation.get('analysis', {})
        
        # Calculate severity score
        severity_factors = {
            'critical_issues': len(analysis.get('critical_issues', [])) * 1.0,
            'high_risk_projects': len(analysis.get('high_risk_projects', [])) * 0.7,
            'anomalies': len(analysis.get('anomalies', [])) * 0.5,
            'trend_negative': len([t for t in analysis.get('trends', []) if t.get('direction') == 'negative']) * 0.6
        }
        
        total_severity = sum(severity_factors.values())
        normalized_severity = min(total_severity / 10.0, 1.0)  # Normalize to 0-1
        
        # Determine alert level
        if normalized_severity >= 0.8:
            alert_level = "critical"
            should_alert = True
            reasoning = f"Critical severity detected ({normalized_severity:.2f}): Multiple critical issues and anomalies present"
        elif normalized_severity >= 0.6:
            alert_level = "high"
            should_alert = True
            reasoning = f"High severity detected ({normalized_severity:.2f}): Significant issues requiring attention"
        elif normalized_severity >= 0.4:
            alert_level = "medium"
            should_alert = True
            reasoning = f"Medium severity detected ({normalized_severity:.2f}): Some issues need monitoring"
        else:
            alert_level = "low"
            should_alert = False
            reasoning = f"Low severity ({normalized_severity:.2f}): No immediate action required"
        
        confidence = self._calculate_confidence(severity_factors)
        
        return {
            'should_alert': should_alert,
            'alert_level': alert_level,
            'severity_score': normalized_severity,
            'confidence': confidence,
            'reasoning': reasoning,
            'factors': severity_factors
        }
    
    def determine_reporting_strategy(self, situation: Dict[str, Any]) -> Dict[str, Any]:
        """
        Determine the best reporting strategy based on the situation
        """
        self.logger.info("📊 Determining reporting strategy...")
        
        analysis = situation.get('analysis', {})
        severity_score = analysis.get('overall_severity_score', 0.5)
        
        # Determine reporting frequency and format
        if severity_score >= 0.8:
            strategy = "immediate_detailed"
            frequency = "immediate"
            format_type = "comprehensive"
            reasoning = "Critical situation requires immediate detailed reporting with full analysis"
        elif severity_score >= 0.6:
            strategy = "urgent_summary"
            frequency = "urgent"
            format_type = "enhanced"
            reasoning = "High severity situation requires urgent reporting with enhanced insights"
        elif severity_score >= 0.4:
            strategy = "standard_report"
            frequency = "scheduled"
            format_type = "standard"
            reasoning = "Standard reporting sufficient for current situation"
        else:
            strategy = "minimal_update"
            frequency = "daily"
            format_type = "summary"
            reasoning = "Minimal update sufficient for low-risk situation"
        
        # Add AI-enhanced features
        ai_features = []
        if analysis.get('anomalies'):
            ai_features.append("anomaly_detection")
        if analysis.get('predictions'):
            ai_features.append("predictive_insights")
        if analysis.get('trends'):
            ai_features.append("trend_analysis")
        
        confidence = self._calculate_confidence({'severity_score': severity_score})
        
        return {
            'strategy': strategy,
            'frequency': frequency,
            'format': format_type,
            'ai_features': ai_features,
            'confidence': confidence,
            'reasoning': reasoning
        }
    
    def recommend_immediate_actions(self, situation: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recommend immediate actions for critical situations
        """
        self.logger.info("⚡ Recommending immediate actions...")
        
        analysis = situation.get('analysis', {})
        critical_issues = analysis.get('critical_issues', [])
        
        actions = []
        
        for issue in critical_issues:
            project_name = issue.get('project', 'Unknown')
            issue_type = issue.get('type', 'performance')
            
            if issue_type == 'budget_overrun':
                action = {
                    'project': project_name,
                    'action': 'immediate_budget_review',
                    'priority': 'critical',
                    'deadline': '2_hours',
                    'responsible_team': 'finance',
                    'description': f"Immediate budget review required for {project_name} due to critical overrun"
                }
            elif issue_type == 'cpu_overload':
                action = {
                    'project': project_name,
                    'action': 'scale_resources',
                    'priority': 'critical',
                    'deadline': '1_hour',
                    'responsible_team': 'infrastructure',
                    'description': f"Immediate scaling required for {project_name} due to CPU overload"
                }
            elif issue_type == 'security_risk':
                action = {
                    'project': project_name,
                    'action': 'security_incident_response',
                    'priority': 'critical',
                    'deadline': '30_minutes',
                    'responsible_team': 'security',
                    'description': f"Security incident response required for {project_name}"
                }
            else:
                action = {
                    'project': project_name,
                    'action': 'investigate_issue',
                    'priority': 'high',
                    'deadline': '4_hours',
                    'responsible_team': 'operations',
                    'description': f"Investigation required for {project_name} - {issue_type}"
                }
            
            actions.append(action)
        
        # Add proactive recommendations based on trends
        if analysis.get('trends'):
            negative_trends = [t for t in analysis['trends'] if t.get('direction') == 'negative']
            for trend in negative_trends:
                action = {
                    'project': trend.get('project', 'Multiple'),
                    'action': 'proactive_monitoring',
                    'priority': 'medium',
                    'deadline': '24_hours',
                    'responsible_team': 'monitoring',
                    'description': f"Proactive monitoring recommended due to negative trend: {trend.get('description')}"
                }
                actions.append(action)
        
        confidence = self._calculate_confidence({'critical_issues_count': len(critical_issues)})
        
        return {
            'actions': actions,
            'total_actions': len(actions),
            'confidence': confidence,
            'reasoning': f"Recommended {len(actions)} immediate actions based on {len(critical_issues)} critical issues"
        }
    
    def evaluate_escalation_needs(self, situation: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate if escalation to higher management is needed
        """
        self.logger.info("📈 Evaluating escalation needs...")
        
        analysis = situation.get('analysis', {})
        
        escalation_triggers = {
            'multiple_critical_issues': len(analysis.get('critical_issues', [])) > 3,
            'severe_budget_impact': any(issue.get('cost_impact', 0) > 10000 for issue in analysis.get('critical_issues', [])),
            'customer_impact': any(issue.get('customer_impact', False) for issue in analysis.get('critical_issues', [])),
            'repeated_failures': len(analysis.get('repeated_issues', [])) > 0,
            'security_breach': any(issue.get('type') == 'security_risk' for issue in analysis.get('critical_issues', []))
        }
        
        escalation_score = sum(escalation_triggers.values()) / len(escalation_triggers)
        
        if escalation_score >= 0.6:
            should_escalate = True
            escalation_level = "executive"
            reasoning = "Multiple escalation triggers met - requires executive attention"
        elif escalation_score >= 0.4:
            should_escalate = True
            escalation_level = "management"
            reasoning = "Some escalation triggers met - requires management attention"
        else:
            should_escalate = False
            escalation_level = "none"
            reasoning = "No escalation required - situation manageable at current level"
        
        confidence = self._calculate_confidence(escalation_triggers)
        
        return {
            'should_escalate': should_escalate,
            'escalation_level': escalation_level,
            'escalation_score': escalation_score,
            'triggers': escalation_triggers,
            'confidence': confidence,
            'reasoning': reasoning
        }
    
    def _calculate_confidence(self, factors: Dict[str, Any]) -> float:
        """
        Calculate confidence level for a decision
        """
        if not factors:
            return 0.5  # Default confidence
        
        # Simple confidence calculation based on factor completeness
        total_factors = len(factors)
        non_zero_factors = sum(1 for v in factors.values() if v != 0)
        
        base_confidence = non_zero_factors / total_factors if total_factors > 0 else 0.5
        
        # Adjust based on factor values
        factor_sum = sum(abs(v) for v in factors.values() if isinstance(v, (int, float)))
        avg_factor_value = factor_sum / total_factors if total_factors > 0 else 0
        
        # Higher factor values increase confidence
        confidence_adjustment = min(avg_factor_value / 10.0, 0.3)
        
        final_confidence = min(base_confidence + confidence_adjustment, 1.0)
        
        return round(final_confidence, 2)
    
    def get_decision_summary(self) -> Dict[str, Any]:
        """Get summary of decision engine capabilities and current state"""
        return {
            'engine_type': 'AI Decision Engine',
            'criteria': self.criteria.__dict__,
            'decision_rules': list(self.decision_rules.keys()),
            'confidence_threshold': self.criteria.confidence_threshold,
            'risk_tolerance': self.criteria.risk_tolerance
        }
