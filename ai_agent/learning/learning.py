"""
Learning System for AI Agent
Orchestrates pattern matching and prediction for continuous learning
"""

import json
import logging
import pickle
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path

from .pattern_matcher import PatternMatcher, Pattern
from .predictor import Predictor


class LearningSystem:
    """
    Main learning system that enables the AI agent to learn from patterns and make predictions.
    Orchestrates pattern matching and prediction components.
    """

    def __init__(self, learning_data_path: str = "learning_data"):
        self.logger = logging.getLogger(__name__)

        # Learning data storage
        self.learning_data_path = Path(learning_data_path)
        self.learning_data_path.mkdir(exist_ok=True)

        # Initialize modular components
        self.pattern_matcher = PatternMatcher()
        self.predictor = Predictor(min_pattern_confidence=0.6)

        # Knowledge bases
        self.historical_data: List[Dict] = []
        self.decision_outcomes: List[Dict] = []
        self.performance_metrics: List[Dict] = []

        # Learning parameters
        self.learning_enabled = True

        # Load existing knowledge
        self._load_knowledge()

        self.logger.info("LearningSystem initialized with pattern and prediction capabilities")

    def identify_patterns(self, infrastructure_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Identify patterns in the current infrastructure data
        """
        current_patterns = self.pattern_matcher.identify_patterns(infrastructure_data)

        # Store current data for future learning
        self._store_historical_data(infrastructure_data)

        return current_patterns

    def predict_issues(self, infrastructure_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Predict potential future issues based on learned patterns
        """
        predictions = self.predictor.predict_issues(
            infrastructure_data,
            self.pattern_matcher.patterns
        )

        return predictions

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
            'effectiveness': self._evaluate_outcome_effectiveness(actions)
        }

        self.decision_outcomes.append(outcome)

        # Update pattern confidences based on outcomes
        self._update_pattern_confidences(outcome)

        # Save updated knowledge
        self._save_knowledge()

        self.logger.info("Knowledge base updated successfully")

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

    def _evaluate_outcome_effectiveness(self, actions: List[Dict]) -> float:
        """Evaluate the effectiveness of actions taken"""
        if not actions:
            return 0.5  # Neutral effectiveness

        # Count successful actions
        successful_actions = sum(1 for action in actions if action.get('success', True))

        return successful_actions / len(actions)

    def _update_pattern_confidences(self, outcome: Dict):
        """Update pattern confidences based on decision outcomes"""
        effectiveness = outcome['effectiveness']

        # Update patterns based on outcome effectiveness
        for pattern in self.pattern_matcher.patterns:
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
                    self.pattern_matcher.patterns = pickle.load(f)

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

            self.logger.info(f"Loaded knowledge: {len(self.pattern_matcher.patterns)} patterns, {len(self.historical_data)} historical points")

        except Exception as e:
            self.logger.warning(f"Could not load knowledge: {e}")

    def _save_knowledge(self):
        """Save current knowledge to files"""
        try:
            # Save patterns
            patterns_file = self.learning_data_path / "patterns.pkl"
            with open(patterns_file, 'wb') as f:
                pickle.dump(self.pattern_matcher.patterns, f)

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
            'patterns_learned': len(self.pattern_matcher.patterns),
            'historical_data_points': len(self.historical_data),
            'decision_outcomes_recorded': len(self.decision_outcomes),
            'min_pattern_confidence': self.pattern_matcher.min_pattern_confidence,
            'knowledge_base_size': sum([
                len(self.pattern_matcher.patterns),
                len(self.historical_data),
                len(self.decision_outcomes)
            ])
        }
