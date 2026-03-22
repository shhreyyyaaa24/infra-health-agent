"""
Learning package for AI Agent
Provides pattern recognition and prediction capabilities
"""

from .pattern_matcher import PatternMatcher, Pattern
from .predictor import Predictor, Prediction
from .learning import LearningSystem

__all__ = [
    'PatternMatcher',
    'Pattern',
    'Predictor',
    'Prediction',
    'LearningSystem'
]
