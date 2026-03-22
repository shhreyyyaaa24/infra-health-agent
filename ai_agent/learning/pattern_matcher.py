"""
Pattern Matcher for Learning System
Identifies infrastructure patterns from historical data
"""

import logging
from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Pattern:
    """Represents a learned pattern"""
    pattern_type: str
    description: str
    confidence: float
    frequency: int
    last_seen: datetime
    contexts: List[Dict[str, Any]]


class PatternMatcher:
    """Identifies and tracks patterns in infrastructure data"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.patterns: List[Pattern] = []
        self.min_pattern_confidence = 0.6
        self.min_pattern_frequency = 3

    def identify_patterns(self, infrastructure_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Identify patterns in the current infrastructure data
        """
        self.logger.info("🧠 Identifying patterns in infrastructure data...")

        current_patterns = []

        # Analyze patterns across all projects
        all_projects = []
        for projects in infrastructure_data.values():
            all_projects.extend(projects)

        # Pattern 1: Recurring critical issues
        critical_patterns = self._identify_critical_issue_patterns(all_projects)
        current_patterns.extend(critical_patterns)

        # Pattern 2: Performance degradation trends
        performance_patterns = self._identify_performance_patterns(all_projects)
        current_patterns.extend(performance_patterns)

        # Pattern 3: Budget overrun patterns
        budget_patterns = self._identify_budget_patterns(all_projects)
        current_patterns.extend(budget_patterns)

        # Pattern 4: Environment-specific patterns
        env_patterns = self._identify_environment_patterns(infrastructure_data)
        current_patterns.extend(env_patterns)

        # Update pattern knowledge base
        self._update_patterns(current_patterns)

        self.logger.info(f"Identified {len(current_patterns)} patterns")

        return current_patterns

    def _identify_critical_issue_patterns(self, projects: List[Dict]) -> List[Dict]:
        """Identify patterns in critical issues"""
        patterns = []

        critical_projects = [p for p in projects if p['status'] == 'SEVERE']

        if len(critical_projects) >= 2:
            pattern = {
                'type': 'simultaneous_critical_issues',
                'description': f"Multiple critical issues detected ({len(critical_projects)} projects)",
                'confidence': min(0.9, len(critical_projects) * 0.2),
                'severity': 'high',
                'projects': [p['name'] for p in critical_projects]
            }
            patterns.append(pattern)

        # Check for specific critical types
        cpu_critical = [p for p in critical_projects if p.get('cpu', 0) > p.get('cpusShutdownLimit', 90)]
        budget_critical = [p for p in critical_projects if p.get('overbudgetProjection', 0) > 1000]

        if len(cpu_critical) >= 2:
            pattern = {
                'type': 'widespread_cpu_issues',
                'description': f"Widespread CPU issues ({len(cpu_critical)} projects)",
                'confidence': min(0.8, len(cpu_critical) * 0.25),
                'severity': 'critical',
                'projects': [p['name'] for p in cpu_critical]
            }
            patterns.append(pattern)

        if len(budget_critical) >= 2:
            pattern = {
                'type': 'widespread_budget_issues',
                'description': f"Widespread budget overruns ({len(budget_critical)} projects)",
                'confidence': min(0.8, len(budget_critical) * 0.25),
                'severity': 'high',
                'projects': [p['name'] for p in budget_critical]
            }
            patterns.append(pattern)

        return patterns

    def _identify_performance_patterns(self, projects: List[Dict]) -> List[Dict]:
        """Identify performance-related patterns"""
        patterns = []

        high_cpu_projects = [p for p in projects if p.get('cpu', 0) > 70]

        if len(high_cpu_projects) >= len(projects) * 0.5:
            pattern = {
                'type': 'general_performance_degradation',
                'description': f"General performance degradation ({len(high_cpu_projects)}/{len(projects)} projects with high CPU)",
                'confidence': 0.7,
                'severity': 'medium',
                'affected_projects': len(high_cpu_projects)
            }
            patterns.append(pattern)

        return patterns

    def _identify_budget_patterns(self, projects: List[Dict]) -> List[Dict]:
        """Identify budget-related patterns"""
        patterns = []

        overbudget_projects = [p for p in projects if p.get('overbudgetProjection', 0) > 0]

        if len(overbudget_projects) >= len(projects) * 0.3:
            pattern = {
                'type': 'widespread_budget_pressure',
                'description': f"Widespread budget pressure ({len(overbudget_projects)}/{len(projects)} projects over budget)",
                'confidence': 0.6,
                'severity': 'medium',
                'affected_projects': len(overbudget_projects)
            }
            patterns.append(pattern)

        return patterns

    def _identify_environment_patterns(self, infrastructure_data: Dict[str, Any]) -> List[Dict]:
        """Identify environment-specific patterns"""
        patterns = []

        for env_name, projects in infrastructure_data.items():
            critical_count = len([p for p in projects if p['status'] == 'SEVERE'])

            if critical_count >= 2:
                pattern = {
                    'type': 'environment_specific_issues',
                    'description': f"Multiple issues in {env_name} environment ({critical_count} critical projects)",
                    'confidence': 0.7,
                    'severity': 'high',
                    'environment': env_name,
                    'critical_count': critical_count
                }
                patterns.append(pattern)

        return patterns

    def _update_patterns(self, current_patterns: List[Dict]):
        """Update pattern knowledge base with new patterns"""
        for pattern_data in current_patterns:
            # Check if pattern already exists
            existing_pattern = None
            for pattern in self.patterns:
                if (pattern.pattern_type == pattern_data['type'] and 
                    pattern.description == pattern_data['description']):
                    existing_pattern = pattern
                    break

            if existing_pattern:
                # Update existing pattern
                existing_pattern.frequency += 1
                existing_pattern.last_seen = datetime.now()
                existing_pattern.confidence = min(0.95, existing_pattern.confidence + 0.05)
            else:
                # Create new pattern
                new_pattern = Pattern(
                    pattern_type=pattern_data['type'],
                    description=pattern_data['description'],
                    confidence=pattern_data['confidence'],
                    frequency=1,
                    last_seen=datetime.now(),
                    contexts=[pattern_data]
                )
                self.patterns.append(new_pattern)

        # Remove old patterns with low confidence
        self.patterns = [
            p for p in self.patterns 
            if p.confidence >= 0.3 or 
            (datetime.now() - p.last_seen).days < 30
        ]

    def pattern_conditions_met(self, pattern: Pattern, infrastructure_data: Dict[str, Any]) -> bool:
        """Check if conditions for a pattern are met in current data"""
        if pattern.pattern_type == 'simultaneous_critical_issues':
            all_projects = []
            for projects in infrastructure_data.values():
                all_projects.extend(projects)

            critical_count = len([p for p in all_projects if p['status'] == 'SEVERE'])
            return critical_count >= 2

        return False
