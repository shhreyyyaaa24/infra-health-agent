"""
Anomaly Detector for Infrastructure Analysis
Detects unusual patterns in CPU and budget metrics
"""

import logging
from typing import Dict, Optional, Tuple
from dataclasses import dataclass


@dataclass
class Anomaly:
    """Represents a detected anomaly"""
    project: str
    metric: str
    value: float
    expected_range: Tuple[float, float]
    severity: str
    description: str
    confidence: float


class AnomalyDetector:
    """Detects anomalies in infrastructure metrics"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.anomaly_threshold = 2.0  # Standard deviations

    def detect_cpu_anomaly(self, project: Dict) -> Optional[Anomaly]:
        """Detect CPU usage anomalies"""
        cpu_usage = project.get('cpu', 0)
        cpu_budget = project.get('cpusBudget', 100)

        # Expected range is 0-80% of budget
        expected_max = cpu_budget * 0.8
        expected_min = 0

        if cpu_usage > expected_max:
            severity = 'critical' if cpu_usage > cpu_budget else 'high'
            return Anomaly(
                project=project['name'],
                metric='cpu_usage',
                value=cpu_usage,
                expected_range=(expected_min, expected_max),
                severity=severity,
                description=f"CPU usage ({cpu_usage}%) exceeds expected range (0-{expected_max}%)",
                confidence=0.9
            )

        return None

    def detect_budget_anomaly(self, project: Dict) -> Optional[Anomaly]:
        """Detect budget anomalies"""
        overbudget = project.get('overbudgetProjection', 0)

        if overbudget > 0:
            # Calculate severity based on amount
            if overbudget > 1000:
                severity = 'critical'
            elif overbudget > 500:
                severity = 'high'
            else:
                severity = 'medium'

            return Anomaly(
                project=project['name'],
                metric='budget_overrun',
                value=overbudget,
                expected_range=(0, 0),
                severity=severity,
                description=f"Budget overrun of ${overbudget} detected",
                confidence=0.8
            )

        return None

    def detect_all_anomalies(self, project: Dict) -> list[Anomaly]:
        """Detect all anomalies for a project"""
        anomalies = []

        cpu_anomaly = self.detect_cpu_anomaly(project)
        if cpu_anomaly:
            anomalies.append(cpu_anomaly)

        budget_anomaly = self.detect_budget_anomaly(project)
        if budget_anomaly:
            anomalies.append(budget_anomaly)

        return anomalies
