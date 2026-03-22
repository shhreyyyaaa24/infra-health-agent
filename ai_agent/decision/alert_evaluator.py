"""
Alert Evaluator for Decision Engine
Assesses alert severity and determines response levels
"""

import logging
from typing import Dict, Any


class AlertEvaluator:
    """Evaluates alert severity and response recommendations"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

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

    def _calculate_confidence(self, factors: Dict[str, Any]) -> float:
        """Calculate confidence level for threshold"""
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
