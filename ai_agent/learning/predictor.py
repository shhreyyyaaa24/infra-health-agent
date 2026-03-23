"""
Predictor for Learning System
Generates predictions based on patterns and trends
"""

import logging
from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Prediction:
    """Represents a prediction made by the learning system"""
    prediction_type: str
    description: str
    confidence: float
    time_horizon: str
    impact_level: str
    recommended_actions: List[str]


class Predictor:
    """Generates predictions based on learned patterns and trends"""

    def __init__(self, min_pattern_confidence: float = 0.6):
        self.logger = logging.getLogger(__name__)
        self.min_pattern_confidence = min_pattern_confidence

    def predict_issues(self, infrastructure_data: Dict[str, Any], patterns: List[Any]) -> List[Dict[str, Any]]:
        """
        Predict potential future issues based on learned patterns
        """
        self.logger.info("🔮 Predicting potential future issues...")

        predictions = []

        # Predict based on historical patterns
        pattern_predictions = self._predict_from_patterns(infrastructure_data, patterns)
        predictions.extend(pattern_predictions)

        # Predict based on trends
        trend_predictions = self._predict_from_trends(infrastructure_data)
        predictions.extend(trend_predictions)

        # Predict based on seasonal patterns
        seasonal_predictions = self._predict_seasonal_issues(infrastructure_data)
        predictions.extend(seasonal_predictions)

        # Filter predictions by confidence
        high_confidence_predictions = [
            p for p in predictions 
            if p['confidence'] >= self.min_pattern_confidence
        ]

        self.logger.info(f"Generated {len(high_confidence_predictions)} high-confidence predictions")

        return high_confidence_predictions

    def _predict_from_patterns(self, infrastructure_data: Dict[str, Any], patterns: List[Any]) -> List[Dict]:
        """Make predictions based on known patterns"""
        predictions = []

        for pattern in patterns:
            if hasattr(pattern, 'confidence') and pattern.confidence >= self.min_pattern_confidence:
                # Check if pattern conditions are met
                prediction = {
                    'type': 'pattern_based',
                    'description': f"Likely to recur: {pattern.description}",
                    'confidence': pattern.confidence,
                    'time_horizon': '24-48_hours',
                    'impact_level': 'medium' if pattern.pattern_type != 'widespread_cpu_issues' else 'high',
                    'pattern_type': pattern.pattern_type
                }
                predictions.append(prediction)

        return predictions

    def _predict_from_trends(self, infrastructure_data: Dict[str, Any]) -> List[Dict]:
        """Make predictions based on current trends"""
        predictions = []

        all_projects = []
        for projects in infrastructure_data.values():
            all_projects.extend(projects)

        # Predict CPU-related issues
        high_cpu_projects = [p for p in all_projects if p.get('cpu', 0) > 80]
        medium_cpu_projects = [p for p in all_projects if 60 < p.get('cpu', 0) <= 80]

        if len(medium_cpu_projects) > 0:
            # Some medium CPU projects might become critical
            escalation_risk = len(medium_cpu_projects) * 0.3  # 30% chance of escalation

            if escalation_risk >= 1:
                prediction = {
                    'type': 'trend_based',
                    'description': f"Risk of CPU escalation in {len(medium_cpu_projects)} medium-usage projects",
                    'confidence': 0.6,
                    'time_horizon': '6-12_hours',
                    'impact_level': 'medium',
                    'at_risk_projects': len(medium_cpu_projects)
                }
                predictions.append(prediction)

        return predictions

    def _predict_seasonal_issues(self, infrastructure_data: Dict[str, Any]) -> List[Dict]:
        """Make predictions based on seasonal patterns"""
        predictions = []

        # Simple seasonal prediction based on day of week
        current_day = datetime.now().weekday()

        # Typically higher load on weekdays (0-4)
        if current_day in [0, 1]:  # Monday, Tuesday
            prediction = {
                'type': 'seasonal',
                'description': "Higher infrastructure load expected early in the week",
                'confidence': 0.5,
                'time_horizon': '2-3_days',
                'impact_level': 'low'
            }
            predictions.append(prediction)

        return predictions
