"""
Trend Analyzer for Infrastructure Analysis
Analyzes performance trends and patterns over time
"""

import logging
from typing import Dict, Optional
from dataclasses import dataclass


@dataclass
class Trend:
    """Represents a detected trend"""
    project: str
    metric: str
    direction: str  # 'positive', 'negative', 'stable'
    strength: float
    description: str
    time_period: str


class TrendAnalyzer:
    """Analyzes trends in infrastructure metrics"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.trend_window = 7  # Days

    def analyze_cpu_trend(self, project: Dict) -> Optional[Trend]:
        """Analyze CPU usage trends (simplified version)"""
        # In real implementation, this would use historical data
        cpu_usage = project.get('cpu', 0)

        # Simulate trend detection based on current usage
        if cpu_usage > 80:
            direction = 'negative'
            strength = min((cpu_usage - 80) / 20.0, 1.0)
            description = f"High CPU usage trend detected ({cpu_usage}%)"
        elif cpu_usage < 30:
            direction = 'positive'
            strength = min((30 - cpu_usage) / 30.0, 1.0)
            description = f"Low CPU usage trend detected ({cpu_usage}%)"
        else:
            direction = 'stable'
            strength = 0.5
            description = f"Stable CPU usage ({cpu_usage}%)"

        return Trend(
            project=project['name'],
            metric='cpu_usage',
            direction=direction,
            strength=strength,
            description=description,
            time_period='current'
        )

    def analyze_budget_trend(self, project: Dict) -> Optional[Trend]:
        """Analyze budget trends"""
        overbudget = project.get('overbudgetProjection', 0)

        if overbudget > 500:
            direction = 'negative'
            strength = min(overbudget / 1000.0, 1.0)
            description = f"Negative budget trend: ${overbudget} projected overrun"
        elif overbudget > 0:
            direction = 'stable'
            strength = 0.5
            description = f"Minor budget pressure: ${overbudget} projected"
        else:
            direction = 'positive'
            strength = 0.5
            description = "Budget within projections"

        return Trend(
            project=project['name'],
            metric='budget',
            direction=direction,
            strength=strength,
            description=description,
            time_period='current'
        )

    def analyze_all_trends(self, project: Dict) -> list[Trend]:
        """Analyze all trends for a project"""
        trends = []

        cpu_trend = self.analyze_cpu_trend(project)
        if cpu_trend:
            trends.append(cpu_trend)

        budget_trend = self.analyze_budget_trend(project)
        if budget_trend:
            trends.append(budget_trend)

        return trends
