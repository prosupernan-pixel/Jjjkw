"""
Setup Script - Initialize project structure and dependencies
"""
import os
import sys
import subprocess
from pathlib import Path


def create_directories():
    """Create necessary directories"""
    directories = [
        'logs',
        'data',
        'backtest_results',
        'tests',
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✓ Created directory: {directory}")


def install_dependencies():
    """Install Python dependencies"""
    print("\nInstalling dependencies...")
    
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to install dependencies")
        return False


def initialize_database():
    """Initialize database"""
    print("\nInitializing database...")
    
    try:
        from core.database import init_db
        db = init_db()
        print("✓ Database initialized successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to initialize database: {e}")
        print("  Note: Ensure PostgreSQL is running and DATABASE_URL is set")
        return False


def check_environment():
    """Check environment setup"""
    print("\nChecking environment setup...")
    
    checks = {
        '.env': os.path.exists('.env'),
        'MT5': check_mt5_installed(),
        'PostgreSQL': check_postgresql(),
    }
    
    for check_name, result in checks.items():
        status = "✓" if result else "✗"
        print(f"{status} {check_name}")


def check_mt5_installed():
    """Check if MT5 is installed"""
    try:
        import MetaTrader5
        return True
    except ImportError:
        return False


def check_postgresql():
    """Check if PostgreSQL is available"""
    try:
        import psycopg2
        return True
    except ImportError:
        return False


def main():
    """Run setup"""
    print("="*50)
    print("SMC Scalping Bot - Setup")
    print("="*50)
    
    # Create directories
    create_directories()
    
    # Install dependencies
    if not install_dependencies():
        print("Please install dependencies manually: pip install -r requirements.txt")
        return False
    
    # Initialize database (optional)
    initialize_database()
    
    # Check environment
    check_environment()
    
    print("\n" + "="*50)
    print("Setup Complete!")
    print("="*50)
    print("\nNext steps:")
    print("1. Edit .env file with your MT5 and Telegram credentials")
    print("2. Ensure PostgreSQL is running")
    print("3. Run: python main.py")
    print("\n" + "="*50)
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
