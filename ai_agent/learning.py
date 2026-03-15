"""
Learning System for AI Agent
Enables the agent to learn from patterns and improve over time
"""

import json
import logging
import pickle
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
import os


@dataclass
class Pattern:
    """Represents a learned pattern"""
    pattern_type: str
    description: str
    confidence: float
    frequency: int
    last_seen: datetime
    contexts: List[Dict[str, Any]]


@dataclass
class Prediction:
    """Represents a prediction made by the learning system"""
    prediction_type: str
    description: str
    confidence: float
    time_horizon: str
    impact_level: str
    recommended_actions: List[str]


class LearningSystem:
    """
    Learning system that enables the AI agent to learn from patterns and make predictions
    """
    
    def __init__(self, learning_data_path: str = "learning_data"):
        self.logger = logging.getLogger(__name__)
        
        # Learning data storage
        self.learning_data_path = Path(learning_data_path)
        self.learning_data_path.mkdir(exist_ok=True)
        
        # Knowledge bases
        self.patterns: List[Pattern] = []
        self.historical_data: List[Dict] = []
        self.decision_outcomes: List[Dict] = []
        self.performance_metrics: List[Dict] = []
        
        # Learning parameters
        self.min_pattern_confidence = 0.6
        self.min_pattern_frequency = 3
        self.learning_enabled = True
        
        # Load existing knowledge
        self._load_knowledge()
        
        self.logger.info("Learning System initialized with pattern recognition capabilities")
    
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
        
        # Store current data for future learning
        self._store_historical_data(infrastructure_data)
        
        self.logger.info(f"Identified {len(current_patterns)} patterns")
        
        return current_patterns
    
    def predict_issues(self, infrastructure_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Predict potential future issues based on learned patterns
        """
        self.logger.info("🔮 Predicting potential future issues...")
        
        predictions = []
        
        # Predict based on historical patterns
        pattern_predictions = self._predict_from_patterns(infrastructure_data)
        predictions.extend(pattern_predictions)
        
        # Predict based on trends
        trend_predictions = self._predict_from_trends(infrastructure_data)
        predictions.extend(trend_predictions)
        
        # Predict based on seasonal patterns (if enough historical data)
        if len(self.historical_data) > 30:  # Need at least 30 data points
            seasonal_predictions = self._predict_seasonal_issues(infrastructure_data)
            predictions.extend(seasonal_predictions)
        
        # Filter predictions by confidence
        high_confidence_predictions = [
            p for p in predictions 
            if p['confidence'] >= self.min_pattern_confidence
        ]
        
        self.logger.info(f"Generated {len(high_confidence_predictions)} high-confidence predictions")
        
        return high_confidence_predictions
    
    def update_knowledge(self, situation: Dict[str, Any], decisions: List[Dict], actions: List[Dict]):
        """
        Update knowledge base based on decision outcomes
        """
        if not self.learning_enabled:
            return
        
        self.logger.info("📚 Updating knowledge base...")
        
        # Record decision outcomes
        outcome = {
            'timestamp': datetime.now().isoformat(),
            'situation': situation,
            'decisions': decisions,
            'actions': actions,
            'effectiveness': self._evaluate_outcome_effectiveness(situation, actions)
        }
        
        self.decision_outcomes.append(outcome)
        
        # Update pattern confidences based on outcomes
        self._update_pattern_confidences(outcome)
        
        # Save updated knowledge
        self._save_knowledge()
        
        self.logger.info("Knowledge base updated successfully")
    
    def _identify_critical_issue_patterns(self, projects: List[Dict]) -> List[Dict]:
        """Identify patterns in critical issues"""
        patterns = []
        
        critical_projects = [p for p in projects if p['status'] == 'SEVERE']
        
        if len(critical_projects) >= 2:
            # Pattern: Multiple critical issues simultaneously
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
    
    def _predict_from_patterns(self, infrastructure_data: Dict[str, Any]) -> List[Dict]:
        """Make predictions based on known patterns"""
        predictions = []
        
        for pattern in self.patterns:
            if pattern.confidence >= self.min_pattern_confidence:
                # Check if pattern conditions are met
                if self._pattern_conditions_met(pattern, infrastructure_data):
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
    
    def _pattern_conditions_met(self, pattern: Pattern, infrastructure_data: Dict[str, Any]) -> bool:
        """Check if conditions for a pattern are met in current data"""
        # Simplified pattern matching - in real implementation, this would be more sophisticated
        if pattern.pattern_type == 'simultaneous_critical_issues':
            all_projects = []
            for projects in infrastructure_data.values():
                all_projects.extend(projects)
            
            critical_count = len([p for p in all_projects if p['status'] == 'SEVERE'])
            return critical_count >= 2
        
        return False
    
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
    
    def _store_historical_data(self, infrastructure_data: Dict[str, Any]):
        """Store current data for historical analysis"""
        data_point = {
            'timestamp': datetime.now().isoformat(),
            'data': infrastructure_data,
            'summary': self._create_data_summary(infrastructure_data)
        }
        
        self.historical_data.append(data_point)
        
        # Keep only last 100 data points to manage memory
        if len(self.historical_data) > 100:
            self.historical_data = self.historical_data[-100:]
    
    def _create_data_summary(self, infrastructure_data: Dict[str, Any]) -> Dict:
        """Create summary of infrastructure data"""
        total_projects = sum(len(projects) for projects in infrastructure_data.values())
        
        status_counts = {"HEALTHY": 0, "MEDIUM": 0, "SEVERE": 0}
        for projects in infrastructure_data.values():
            for project in projects:
                status_counts[project['status']] += 1
        
        return {
            'total_projects': total_projects,
            'status_counts': status_counts,
            'timestamp': datetime.now().isoformat()
        }
    
    def _evaluate_outcome_effectiveness(self, situation: Dict[str, Any], actions: List[Dict]) -> float:
        """Evaluate the effectiveness of actions taken"""
        # Simplified effectiveness evaluation
        # In real implementation, this would compare before/after metrics
        
        if not actions:
            return 0.5  # Neutral effectiveness
        
        # Count successful actions
        successful_actions = sum(1 for action in actions if action.get('success', True))
        
        return successful_actions / len(actions)
    
    def _update_pattern_confidences(self, outcome: Dict):
        """Update pattern confidences based on decision outcomes"""
        effectiveness = outcome['effectiveness']
        
        # Update patterns that were involved in this decision
        for pattern in self.patterns:
            # Simple confidence update based on outcome effectiveness
            if effectiveness > 0.8:
                pattern.confidence = min(0.95, pattern.confidence + 0.02)
            elif effectiveness < 0.5:
                pattern.confidence = max(0.3, pattern.confidence - 0.02)
    
    def _load_knowledge(self):
        """Load existing knowledge from files"""
        try:
            # Load patterns
            patterns_file = self.learning_data_path / "patterns.pkl"
            if patterns_file.exists():
                with open(patterns_file, 'rb') as f:
                    self.patterns = pickle.load(f)
            
            # Load historical data
            history_file = self.learning_data_path / "history.pkl"
            if history_file.exists():
                with open(history_file, 'rb') as f:
                    self.historical_data = pickle.load(f)
            
            # Load decision outcomes
            outcomes_file = self.learning_data_path / "outcomes.pkl"
            if outcomes_file.exists():
                with open(outcomes_file, 'rb') as f:
                    self.decision_outcomes = pickle.load(f)
            
            self.logger.info(f"Loaded knowledge: {len(self.patterns)} patterns, {len(self.historical_data)} historical points")
            
        except Exception as e:
            self.logger.warning(f"Could not load knowledge: {e}")
    
    def _save_knowledge(self):
        """Save current knowledge to files"""
        try:
            # Save patterns
            patterns_file = self.learning_data_path / "patterns.pkl"
            with open(patterns_file, 'wb') as f:
                pickle.dump(self.patterns, f)
            
            # Save historical data
            history_file = self.learning_data_path / "history.pkl"
            with open(history_file, 'wb') as f:
                pickle.dump(self.historical_data, f)
            
            # Save decision outcomes
            outcomes_file = self.learning_data_path / "outcomes.pkl"
            with open(outcomes_file, 'wb') as f:
                pickle.dump(self.decision_outcomes, f)
            
            self.logger.info("Knowledge saved successfully")
            
        except Exception as e:
            self.logger.error(f"Could not save knowledge: {e}")
    
    def get_learning_status(self) -> Dict[str, Any]:
        """Get status of the learning system"""
        return {
            'learning_enabled': self.learning_enabled,
            'patterns_learned': len(self.patterns),
            'historical_data_points': len(self.historical_data),
            'decision_outcomes_recorded': len(self.decision_outcomes),
            'min_pattern_confidence': self.min_pattern_confidence,
            'knowledge_base_size': sum([
                len(self.patterns),
                len(self.historical_data),
                len(self.decision_outcomes)
            ])
        }
