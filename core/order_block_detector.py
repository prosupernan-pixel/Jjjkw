"""
Order Block Detector - Identifies entry zones
"""
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)


class OrderBlockDetector:
    """
    Detects Order Blocks (OB) - candles that cause BOS.
    
    Bullish OB:
    - Last bearish candle before bullish impuls
    - High of this candle becomes support
    
    Bearish OB:
    - Last bullish candle before bearish impuls
    - Low of this candle becomes resistance
    """
    
    def __init__(self):
        """Initialize order block detector"""
        self.last_ob = None
        self.ob_history = []
    
    def detect_order_block(self, candles: List[Dict], bos_type: str, 
                          bos_valid: bool) -> Dict:
        """
        Detect Order Block from candle sequence.
        
        Args:
            candles: List of recent candles (at least 3)
            bos_type: 'bullish' or 'bearish' or None
            bos_valid: Is BOS valid
        
        Returns:
            {
                'ob_type': 'bullish' | 'bearish' | None,
                'is_valid': bool,
                'ob_high': float,
                'ob_low': float,
                'ob_range': float,
                'strength': 0-100,
                'candle_index': int,
            }
        """
        
        if not bos_valid or len(candles) < 2:
            return {
                'ob_type': None,
                'is_valid': False,
                'ob_high': None,
                'ob_low': None,
                'ob_range': None,
                'strength': 0,
                'candle_index': -1,
            }
        
        if bos_type == 'bullish':
            return self._detect_bullish_ob(candles)
        elif bos_type == 'bearish':
            return self._detect_bearish_ob(candles)
        
        return {
            'ob_type': None,
            'is_valid': False,
            'ob_high': None,
            'ob_low': None,
            'ob_range': None,
            'strength': 0,
            'candle_index': -1,
        }
    
    def _detect_bullish_ob(self, candles: List[Dict]) -> Dict:
        """
        Detect bullish order block.
        
        The last bearish candle before bullish breakout.
        Its high becomes support zone.
        """
        
        if len(candles) < 2:
            return {
                'ob_type': None,
                'is_valid': False,
                'ob_high': None,
                'ob_low': None,
                'ob_range': None,
                'strength': 0,
                'candle_index': -1,
            }
        
        # Find last bearish candle
        ob_candle = None
        ob_index = -1
        
        for i in range(len(candles) - 1, -1, -1):
            candle = candles[i]
            # Bearish candle (close < open)
            if candle['c'] < candle['o']:
                ob_candle = candle
                ob_index = i
                break
        
        if ob_candle is None:
            return {
                'ob_type': None,
                'is_valid': False,
                'ob_high': None,
                'ob_low': None,
                'ob_range': None,
                'strength': 0,
                'candle_index': -1,
            }
        
        # Calculate range and strength
        ob_range = ob_candle['h'] - ob_candle['l']
        body = ob_candle['o'] - ob_candle['c']
        body_ratio = body / (ob_range if ob_range > 0 else 1)
        strength = min(100, body_ratio * 100)
        
        self.last_ob = {
            'type': 'bullish',
            'high': ob_candle['h'],
            'low': ob_candle['l'],
        }
        
        return {
            'ob_type': 'bullish',
            'is_valid': True,
            'ob_high': ob_candle['h'],
            'ob_low': ob_candle['l'],
            'ob_range': ob_range,
            'strength': strength,
            'candle_index': ob_index,
        }
    
    def _detect_bearish_ob(self, candles: List[Dict]) -> Dict:
        """
        Detect bearish order block.
        
        The last bullish candle before bearish breakout.
        Its low becomes resistance zone.
        """
        
        if len(candles) < 2:
            return {
                'ob_type': None,
                'is_valid': False,
                'ob_high': None,
                'ob_low': None,
                'ob_range': None,
                'strength': 0,
                'candle_index': -1,
            }
        
        # Find last bullish candle
        ob_candle = None
        ob_index = -1
        
        for i in range(len(candles) - 1, -1, -1):
            candle = candles[i]
            # Bullish candle (close > open)
            if candle['c'] > candle['o']:
                ob_candle = candle
                ob_index = i
                break
        
        if ob_candle is None:
            return {
                'ob_type': None,
                'is_valid': False,
                'ob_high': None,
                'ob_low': None,
                'ob_range': None,
                'strength': 0,
                'candle_index': -1,
            }
        
        # Calculate range and strength
        ob_range = ob_candle['h'] - ob_candle['l']
        body = ob_candle['c'] - ob_candle['o']
        body_ratio = body / (ob_range if ob_range > 0 else 1)
        strength = min(100, body_ratio * 100)
        
        self.last_ob = {
            'type': 'bearish',
            'high': ob_candle['h'],
            'low': ob_candle['l'],
        }
        
        return {
            'ob_type': 'bearish',
            'is_valid': True,
            'ob_high': ob_candle['h'],
            'ob_low': ob_candle['l'],
            'ob_range': ob_range,
            'strength': strength,
            'candle_index': ob_index,
        }
    
    def is_price_at_ob(self, price: float, ob_info: Dict, threshold: float = 0.001) -> bool:
        """
        Check if price is at order block (within threshold).
        
        Args:
            price: Current price
            ob_info: Order block info
            threshold: Percentage threshold (default 0.1%)
        """
        
        if not ob_info.get('is_valid'):
            return False
        
        ob_high = ob_info.get('ob_high')
        ob_low = ob_info.get('ob_low')
        ob_range = ob_info.get('ob_range', 0)
        
        if ob_range == 0:
            return False
        
        threshold_pips = ob_range * threshold
        
        return (ob_low - threshold_pips) <= price <= (ob_high + threshold_pips)
    
    def get_ob_level(self, ob_type: str) -> float:
        """Get the OB level based on type"""
        if self.last_ob is None:
            return None
        
        if ob_type == 'bullish':
            return self.last_ob.get('high')
        elif ob_type == 'bearish':
            return self.last_ob.get('low')
        
        return None
