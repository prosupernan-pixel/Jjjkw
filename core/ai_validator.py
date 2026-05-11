"""
AI Validator - Scores trade setups using multi-factor analysis
"""
import logging
from typing import Dict

logger = logging.getLogger(__name__)


class AIValidator:
    """
    Validates trade setups using AI scoring system.
    
    Factors:
    - BOS strength (25%)
    - IDM quality (20%)
    - OB reaction (20%)
    - Volume (15%)
    - Trend momentum (20%)
    
    Score 0-100:
    - 85+: Strong entry
    - 70-84: Medium entry
    - <70: Skip
    """
    
    def __init__(self):
        """Initialize AI validator"""
        self.weights = {
            'bos': 0.25,
            'idm': 0.20,
            'ob': 0.20,
            'volume': 0.15,
            'momentum': 0.20,
        }
    
    def validate_setup(self, setup: Dict) -> Dict:
        """
        Validate complete trade setup and generate AI score.
        
        Args:
            setup: {
                'trend': 'bullish'|'bearish',
                'bos': {'strength': 0-100, 'valid': bool},
                'idm': {'strength': 0-100, 'valid': bool},
                'ob': {'strength': 0-100, 'valid': bool},
                'volume': {'increase': 0-100, 'valid': bool},
                'momentum': {'strength': 0-100, 'valid': bool},
            }
        
        Returns:
            {
                'score': 0-100,
                'rating': 'strong'|'medium'|'weak',
                'factors': {...},
                'recommendation': 'BUY'|'SELL'|'SKIP',
                'confidence': 0-100,
            }
        """
        
        factors = {
            'bos': self._score_bos(setup.get('bos', {})),
            'idm': self._score_idm(setup.get('idm', {})),
            'ob': self._score_ob(setup.get('ob', {})),
            'volume': self._score_volume(setup.get('volume', {})),
            'momentum': self._score_momentum(setup.get('momentum', {})),
        }
        
        # Calculate weighted score
        total_score = 0
        for factor, score in factors.items():
            total_score += score * self.weights[factor]
        
        total_score = min(100, max(0, total_score))
        
        # Determine rating
        if total_score >= 85:
            rating = 'strong'
            confidence = min(100, total_score + 5)
        elif total_score >= 70:
            rating = 'medium'
            confidence = total_score
        else:
            rating = 'weak'
            confidence = total_score
        
        # Get recommendation
        trend = setup.get('trend', 'unknown')
        if rating == 'weak':
            recommendation = 'SKIP'
        elif trend == 'bullish':
            recommendation = 'BUY'
        elif trend == 'bearish':
            recommendation = 'SELL'
        else:
            recommendation = 'SKIP'
        
        return {
            'score': total_score,
            'rating': rating,
            'factors': factors,
            'recommendation': recommendation,
            'confidence': confidence,
        }
    
    def _score_bos(self, bos: Dict) -> float:
        """Score Break of Structure"""
        
        if not bos.get('valid', False):
            return 20  # Invalid BOS but not zero
        
        strength = bos.get('strength', 0)
        
        # BOS strength is critical
        if strength >= 80:
            return 95
        elif strength >= 60:
            return 75
        elif strength >= 40:
            return 50
        else:
            return 30
    
    def _score_idm(self, idm: Dict) -> float:
        """Score Inducement quality"""
        
        if not idm.get('valid', False):
            return 25  # Some points for structure
        
        strength = idm.get('strength', 0)
        has_rejection = idm.get('rejection', False)
        
        base_score = strength
        
        # Bonus for rejection confirmation
        if has_rejection:
            base_score += 15
        
        return min(100, base_score)
    
    def _score_ob(self, ob: Dict) -> float:
        """Score Order Block quality"""
        
        if not ob.get('valid', False):
            return 30  # Some base score
        
        strength = ob.get('strength', 0)
        proximity = ob.get('proximity', 0)  # How close price is to OB
        
        # OB strength + proximity to price
        base_score = strength * 0.7 + proximity * 30
        
        return min(100, base_score)
    
    def _score_volume(self, volume: Dict) -> float:
        """Score Volume confirmation"""
        
        if not volume.get('valid', False):
            return 40  # Neutral score
        
        increase = volume.get('increase', 0)
        
        # Volume should increase significantly
        if increase >= 2.0:  # 100% increase
            return 95
        elif increase >= 1.5:  # 50% increase
            return 75
        elif increase >= 1.2:  # 20% increase
            return 55
        else:
            return 35
    
    def _score_momentum(self, momentum: Dict) -> float:
        """Score Trend momentum"""
        
        if not momentum.get('valid', False):
            return 30
        
        strength = momentum.get('strength', 0)
        
        # Momentum shows conviction
        if strength >= 70:
            return 90
        elif strength >= 50:
            return 70
        else:
            return 45
    
    def should_enter(self, score: float, min_threshold: float = 70) -> bool:
        """Check if score meets minimum threshold"""
        return score >= min_threshold
    
    def is_strong_entry(self, score: float) -> bool:
        """Check if score indicates strong entry"""
        return score >= 85
    
    def is_medium_entry(self, score: float) -> bool:
        """Check if score indicates medium entry"""
        return 70 <= score < 85
    
    def get_score_explanation(self, score: float) -> str:
        """Get human-readable explanation of score"""
        
        if score >= 85:
            return "STRONG ENTRY - High probability setup"
        elif score >= 70:
            return "MEDIUM ENTRY - Reasonable probability setup"
        elif score >= 50:
            return "WEAK ENTRY - Lower probability setup"
        else:
            return "SKIP - Poor setup, avoid trading"
