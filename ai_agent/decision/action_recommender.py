"""
Action Recommender for Decision Engine
Generates immediate actions and escalation recommendations
"""

import logging
from typing import Dict, List, Any


class ActionRecommender:
    """Recommends immediate actions for critical situations"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

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

            action = self._create_action_for_issue(project_name, issue_type)
            actions.append(action)

        # Add proactive recommendations based on trends
        if analysis.get('trends'):
            trend_actions = self._create_trend_actions(analysis['trends'])
            actions.extend(trend_actions)

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

    def _create_action_for_issue(self, project_name: str, issue_type: str) -> Dict[str, Any]:
        """Create action recommendation for specific issue type"""
        if issue_type == 'budget_overrun':
            return {
                'project': project_name,
                'action': 'immediate_budget_review',
                'priority': 'critical',
                'deadline': '2_hours',
                'responsible_team': 'finance',
                'description': f"Immediate budget review required for {project_name} due to critical overrun"
            }
        elif issue_type == 'cpu_overload':
            return {
                'project': project_name,
                'action': 'scale_resources',
                'priority': 'critical',
                'deadline': '1_hour',
                'responsible_team': 'infrastructure',
                'description': f"Immediate scaling required for {project_name} due to CPU overload"
            }
        elif issue_type == 'security_risk':
            return {
                'project': project_name,
                'action': 'security_incident_response',
                'priority': 'critical',
                'deadline': '30_minutes',
                'responsible_team': 'security',
                'description': f"Security incident response required for {project_name}"
            }
        else:
            return {
                'project': project_name,
                'action': 'investigate_issue',
                'priority': 'high',
                'deadline': '4_hours',
                'responsible_team': 'operations',
                'description': f"Investigation required for {project_name} - {issue_type}"
            }

    def _create_trend_actions(self, trends: List[Dict]) -> List[Dict[str, Any]]:
        """Create actions for negative trends"""
        actions = []

        negative_trends = [t for t in trends if t.get('direction') == 'negative']
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

        return actions

    def _calculate_confidence(self, factors: Dict[str, Any]) -> float:
        """Calculate confidence level for recommendation"""
        if not factors:
            return 0.5

        total_factors = len(factors)
        non_zero_factors = sum(1 for v in factors.values() if v != 0)

        base_confidence = non_zero_factors / total_factors if total_factors > 0 else 0.5

        factor_sum = sum(abs(v) for v in factors.values() if isinstance(v, (int, float)))
        avg_factor_value = factor_sum / total_factors if total_factors > 0 else 0

        confidence_adjustment = min(avg_factor_value / 10.0, 0.3)
        final_confidence = min(base_confidence + confidence_adjustment, 1.0)

        return round(final_confidence, 2)
