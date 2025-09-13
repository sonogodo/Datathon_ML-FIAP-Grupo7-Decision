"""
Configurações do sistema Decision AI
"""
import os
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent
DATA_PATH = PROJECT_ROOT / "data"
MODELS_PATH = PROJECT_ROOT / "models"
LOGS_PATH = PROJECT_ROOT / "logs"

# Ensure directories exist
DATA_PATH.mkdir(exist_ok=True)
MODELS_PATH.mkdir(exist_ok=True)
LOGS_PATH.mkdir(exist_ok=True)

# Model settings
MODEL_CONFIG = {
    'n_estimators': 100,
    'max_depth': 10,
    'min_samples_split': 5,
    'min_samples_leaf': 2,
    'random_state': 42,
    'class_weight': 'balanced'
}

# API settings
API_CONFIG = {
    'host': '0.0.0.0',
    'port': 8000,
    'reload': False,
    'log_level': 'info'
}

# Feature engineering settings
FEATURE_CONFIG = {
    'drift_threshold': 0.1,
    'min_samples_for_cv': 10,
    'test_size': 0.2,
    'cv_folds': 5
}

# File names
DATA_FILES = {
    'vagas': 'vagas.json',
    'prospects': 'prospects.json',
    'applicants': 'applicants.json'
}

# Environment detection
def is_development():
    """Check if running in development mode"""
    return os.getenv('ENVIRONMENT', 'development') == 'development'

def is_production():
    """Check if running in production mode"""
    return os.getenv('ENVIRONMENT') == 'production'

# Logging configuration
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': str(LOGS_PATH / 'decision_ai.log'),
            'formatter': 'detailed'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG' if is_development() else 'INFO',
            'propagate': False
        }
    }
}