"""
Configuration Settings for SMC Scalping Bot
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ==================== TRADING CONFIG ====================
TRADING_CONFIG = {
    "pair": os.getenv("TRADING_PAIR", "EURUSD"),
    "timeframe": os.getenv("TIMEFRAME", "M5"),
    "trading_enabled": os.getenv("TRADING_ENABLED", "False").lower() == "true",
    "paper_trading": os.getenv("PAPER_TRADING", "True").lower() == "true",
}

# ==================== RISK MANAGEMENT ====================
RISK_CONFIG = {
    "risk_percent": float(os.getenv("RISK_PERCENT", 1.0)),
    "max_daily_dd": float(os.getenv("MAX_DAILY_DD", 5.0)),
    "max_consecutive_loss": int(os.getenv("MAX_CONSECUTIVE_LOSS", 3)),
    "position_size_method": os.getenv("POSITION_SIZE_METHOD", "percent"),
    "rr_minimum": 1.5,
}

# ==================== AI CONFIG ====================
AI_CONFIG = {
    "score_threshold": int(os.getenv("AI_SCORE_THRESHOLD", 70)),
    "strong_entry_threshold": int(os.getenv("STRONG_ENTRY_THRESHOLD", 85)),
    "enable_filter": os.getenv("ENABLE_AI_FILTER", "True").lower() == "true",
    # Weights for scoring
    "bos_weight": 0.25,
    "idm_weight": 0.20,
    "ob_weight": 0.20,
    "volume_weight": 0.15,
    "momentum_weight": 0.20,
}

# ==================== DATABASE CONFIG ====================
DATABASE_CONFIG = {
    "url": os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/smc_bot"),
    "echo": os.getenv("DATABASE_ECHO", "False").lower() == "true",
    "pool_size": 10,
    "max_overflow": 20,
}

# ==================== TELEGRAM CONFIG ====================
TELEGRAM_CONFIG = {
    "bot_token": os.getenv("TELEGRAM_BOT_TOKEN", ""),
    "chat_id": os.getenv("TELEGRAM_CHAT_ID", ""),
    "enabled": os.getenv("ENABLE_TELEGRAM", "True").lower() == "true",
}

# ==================== MT5 CONFIG ====================
MT5_CONFIG = {
    "login": int(os.getenv("MT5_LOGIN", 0)),
    "password": os.getenv("MT5_PASSWORD", ""),
    "server": os.getenv("MT5_SERVER", ""),
    "path": os.getenv("MT5_PATH", "C:\\Program Files\\MetaTrader 5\\terminal64.exe"),
    "timeout": 5000,
}

# ==================== LOGGING CONFIG ====================
LOGGING_CONFIG = {
    "level": os.getenv("LOG_LEVEL", "INFO"),
    "file": os.getenv("LOG_FILE", "logs/bot.log"),
    "max_bytes": 10485760,  # 10MB
    "backup_count": 5,
}

# ==================== SESSION FILTER ====================
SESSION_CONFIG = {
    "enabled": os.getenv("ENABLE_SESSION_FILTER", "True").lower() == "true",
    "preferred_sessions": os.getenv("PREFERRED_SESSIONS", "London,NewYork,Overlap").split(","),
}

# ==================== NEWS FILTER ====================
NEWS_CONFIG = {
    "enabled": os.getenv("ENABLE_NEWS_FILTER", "False").lower() == "true",
    "high_impact_minutes": int(os.getenv("HIGH_IMPACT_NEWS_MINUTES", 60)),
}

# ==================== BACKTESTING ====================
BACKTEST_CONFIG = {
    "enabled": os.getenv("ENABLE_BACKTESTING", "False").lower() == "true",
    "start_date": os.getenv("BACKTEST_START_DATE", "2023-01-01"),
    "end_date": os.getenv("BACKTEST_END_DATE", "2024-01-01"),
}

# ==================== GENERAL ====================
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# ==================== TIMEFRAME MAPPING ====================
TIMEFRAME_MAPPING = {
    "M1": 1,
    "M5": 5,
    "M15": 15,
    "M30": 30,
    "H1": 60,
    "H4": 240,
    "D1": 1440,
}

# ==================== CANDLE PATTERNS ====================
CANDLE_PATTERNS = {
    "pinbar": {
        "wick_ratio": 1.5,  # Wick should be 1.5x body
        "body_ratio": 0.3,  # Body is 30% of total candle
    },
    "engulfing": {
        "body_ratio": 0.8,  # New body engulfs 80%+ of previous body
    },
}

# ==================== SESSION TIMES ====================
SESSION_TIMES = {
    "London": {"open": 8, "close": 17},      # GMT
    "NewYork": {"open": 13, "close": 22},    # GMT
    "Sydney": {"open": 22, "close": 7},      # GMT (next day)
    "Tokyo": {"open": 0, "close": 9},        # GMT
}

# ==================== FIBONACCI LEVELS ====================
FIBONACCI_LEVELS = [0.236, 0.382, 0.5, 0.618, 0.786]

# ==================== TECHNICAL INDICATORS ====================
INDICATORS_CONFIG = {
    "sma_periods": [9, 20, 50],
    "ema_periods": [5, 10, 20],
    "rsi_period": 14,
    "rsi_overbought": 70,
    "rsi_oversold": 30,
    "macd_fast": 12,
    "macd_slow": 26,
    "macd_signal": 9,
    "bb_period": 20,
    "bb_std_dev": 2,
    "atr_period": 14,
}

# ==================== SPREAD CONFIG ====================
SPREAD_CONFIG = {
    "max_spread_pips": 2.5,
    "check_enabled": True,
}

# ==================== VOLUME CONFIG ====================
VOLUME_CONFIG = {
    "min_volume_increase": 1.2,  # 20% increase required
}
