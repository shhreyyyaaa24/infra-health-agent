"""
Decision Engine for AI Agent
Orchestrates decision-making based on analysis and recommendations
"""

import logging
from typing import Dict, List, Any
from dataclasses import dataclass

from .alert_evaluator import AlertEvaluator
from .action_recommender import ActionRecommender


@dataclass
class DecisionCriteria:
    """Criteria for making decisions"""
    severity_threshold: float
    confidence_threshold: float
    risk_tolerance: float
    priority_weights: Dict[str, float]


class DecisionEngine:
    """
    Main decision-making engine that orchestrates alert evaluation and action recommendations.
    Uses modular components for easy extension and maintenance.
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

        # Initialize modular components
        self.alert_evaluator = AlertEvaluator()
        self.action_recommender = ActionRecommender()

        self.logger.info("DecisionEngine initialized with modular components")

    def assess_alert_severity(self, situation: Dict[str, Any]) -> Dict[str, Any]:
        """Assess alert severity using alert evaluator"""
        return self.alert_evaluator.assess_alert_severity(situation)

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
        """Recommend immediate actions using action recommender"""
        return self.action_recommender.recommend_immediate_actions(situation)

    def evaluate_escalation_needs(self, situation: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate escalation needs using action recommender"""
        return self.action_recommender.evaluate_escalation_needs(situation)

    def _calculate_confidence(self, factors: Dict[str, Any]) -> float:
        """
        Calculate confidence level for a decision
        """
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

    def get_decision_summary(self) -> Dict[str, Any]:
        """Get summary of decision engine capabilities and current state"""
        return {
            'engine_type': 'AI Decision Engine',
            'criteria': self.criteria.__dict__,
            'confidence_threshold': self.criteria.confidence_threshold,
            'risk_tolerance': self.criteria.risk_tolerance
        }
