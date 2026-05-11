"""
Risk Manager - Position sizing and risk management
"""
import logging
from typing import Dict

logger = logging.getLogger(__name__)


class RiskManager:
    """
    Manages position sizing, risk, and trade management.
    
    Rules:
    - 1% risk per trade
    - 5% max daily drawdown
    - 3 max consecutive losses
    - 1 position per pair
    """
    
    def __init__(self, account_balance: float = 10000):
        """
        Initialize risk manager.
        
        Args:
            account_balance: Starting balance
        """
        self.account_balance = account_balance
        self.daily_pnl = 0
        self.consecutive_losses = 0
        self.active_positions = {}
        self.trade_history = []
        
        # Risk config
        self.risk_percent = 1.0
        self.max_daily_dd = 5.0
        self.max_consecutive_loss = 3
        self.rr_minimum = 1.5
    
    def can_trade(self) -> bool:
        """Check if trading is allowed"""
        
        # Check daily drawdown
        dd_percent = (abs(self.daily_pnl) / self.account_balance) * 100
        if self.daily_pnl < 0 and dd_percent >= self.max_daily_dd:
            logger.warning(f"Daily DD limit reached: {dd_percent:.2f}%")
            return False
        
        # Check consecutive losses
        if self.consecutive_losses >= self.max_consecutive_loss:
            logger.warning(f"Max consecutive losses reached: {self.consecutive_losses}")
            return False
        
        return True
    
    def calculate_position_size(self, entry_price: float, stop_loss: float,
                               take_profit: float = None) -> Dict:
        """
        Calculate position size based on risk and SL.
        
        Args:
            entry_price: Entry price
            stop_loss: Stop loss price
            take_profit: Take profit price (optional)
        
        Returns:
            {
                'position_size': float,
                'risk_amount': float,
                'rr': float,
                'is_valid': bool,
            }
        """
        
        if entry_price == stop_loss:
            return {
                'position_size': 0,
                'risk_amount': 0,
                'rr': 0,
                'is_valid': False,
            }
        
        # Calculate risk amount (1% of account)
        risk_amount = self.account_balance * (self.risk_percent / 100)
        
        # Calculate pips to SL
        pips_to_sl = abs(entry_price - stop_loss)
        
        # Position size = risk amount / pips to SL
        position_size = risk_amount / pips_to_sl if pips_to_sl > 0 else 0
        
        # Calculate RR if TP provided
        rr = 1.0
        if take_profit:
            pips_to_tp = abs(take_profit - entry_price)
            rr = pips_to_tp / pips_to_sl if pips_to_sl > 0 else 0
        
        # Validate
        is_valid = rr >= self.rr_minimum and position_size > 0
        
        if not is_valid:
            logger.warning(f"Position invalid: RR={rr:.2f}, Size={position_size}")
        
        return {
            'position_size': position_size,
            'risk_amount': risk_amount,
            'rr': rr,
            'is_valid': is_valid,
        }
    
    def open_position(self, symbol: str, direction: str, entry: float,
                     stop_loss: float, take_profit: float,
                     position_size: float) -> Dict:
        """
        Open a new position.
        
        Args:
            symbol: Trading pair
            direction: 'BUY' or 'SELL'
            entry: Entry price
            stop_loss: Stop loss price
            take_profit: Take profit price
            position_size: Position size
        
        Returns:
            Position info
        """
        
        # Check if already have position in this symbol
        if symbol in self.active_positions:
            logger.warning(f"Already have open position in {symbol}")
            return None
        
        position = {
            'symbol': symbol,
            'direction': direction,
            'entry': entry,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'position_size': position_size,
            'profit': 0,
            'profit_percent': 0,
        }
        
        self.active_positions[symbol] = position
        logger.info(f"Opened {direction} {symbol} at {entry}")
        
        return position
    
    def close_position(self, symbol: str, close_price: float,
                      is_profit: bool = True) -> Dict:
        """
        Close a position.
        
        Args:
            symbol: Trading pair
            close_price: Close price
            is_profit: Whether trade was profitable
        
        Returns:
            Trade result
        """
        
        if symbol not in self.active_positions:
            logger.warning(f"No open position in {symbol}")
            return None
        
        position = self.active_positions[symbol]
        
        # Calculate PnL
        if position['direction'] == 'BUY':
            pnl = (close_price - position['entry']) * position['position_size']
        else:
            pnl = (position['entry'] - close_price) * position['position_size']
        
        pnl_percent = (pnl / (position['entry'] * position['position_size'])) * 100
        
        # Update stats
        self.daily_pnl += pnl
        self.trade_history.append({
            'symbol': symbol,
            'direction': position['direction'],
            'entry': position['entry'],
            'close': close_price,
            'pnl': pnl,
            'pnl_percent': pnl_percent,
        })
        
        # Update consecutive losses
        if is_profit:
            self.consecutive_losses = 0
        else:
            self.consecutive_losses += 1
        
        # Remove from active
        del self.active_positions[symbol]
        
        logger.info(f"Closed {symbol}: PnL=${pnl:.2f} ({pnl_percent:.2f}%)")
        
        return {
            'symbol': symbol,
            'pnl': pnl,
            'pnl_percent': pnl_percent,
            'consecutive_losses': self.consecutive_losses,
        }
    
    def update_position(self, symbol: str, current_price: float) -> Dict:
        """Update position P&L"""
        
        if symbol not in self.active_positions:
            return None
        
        position = self.active_positions[symbol]
        
        if position['direction'] == 'BUY':
            profit = (current_price - position['entry']) * position['position_size']
        else:
            profit = (position['entry'] - current_price) * position['position_size']
        
        profit_percent = (profit / (position['entry'] * position['position_size'])) * 100
        
        position['profit'] = profit
        position['profit_percent'] = profit_percent
        
        return position
    
    def get_drawdown_percent(self) -> float:
        """Get current drawdown percentage"""
        return (abs(self.daily_pnl) / self.account_balance) * 100 if self.daily_pnl < 0 else 0
    
    def get_current_balance(self) -> float:
        """Get current balance including unrealized P&L"""
        unrealized = sum(p['profit'] for p in self.active_positions.values())
        return self.account_balance + self.daily_pnl + unrealized
    
    def get_winrate(self) -> float:
        """Calculate win rate from trade history"""
        if not self.trade_history:
            return 0
        
        wins = sum(1 for trade in self.trade_history if trade['pnl'] > 0)
        return (wins / len(self.trade_history)) * 100
    
    def reset_daily(self):
        """Reset daily stats"""
        self.daily_pnl = 0
        self.consecutive_losses = 0
        logger.info("Daily stats reset")
